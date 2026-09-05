#!/usr/bin/env python3
"""TREE-COL-035 — F-NAR-019. Raphaël, store goutteux, trois mots. COL.POL.001, N2."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-035"
N2 = LIMITS["N2"]
CHILD = "enfant-m"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="croissant d'eau",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=les trois mots veulent partir trop vite; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=le mot s est cassé; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=soulagement_discret; intensite=1; destinataire=enfant; sous_texte=une oreille s est ouverte; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il veut dire les trois mots tout de suite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=l oreille n est pas prête; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=attendre le toc livre les trois mots; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le croissant d eau a trouvé sa place; tempo=posé; sourire=léger; respiration=ample",
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
    out["locale"] = "fr_FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    fields = (extra or {}).get("fields") or {}
    out.update(fields)
    return out


N, E, P, M = "narrateur", CHILD, "papa", "maman"
TICS = ("tout doux", "tout calme", " tout bas", "encore", "déjà")


def assert_clean(script: str, cid: str) -> None:
    low = script.lower()
    for t in TICS:
        if t in low:
            raise SystemExit(f"{cid} tic: {t}")


def t2_scenes() -> dict:
    return {
        ("boulangerie", "boulangere"): (
            L(
                (N, "La boulangère a de la farine jusqu'aux poignets."),
                (N, "Elle compte des pièces, une par une, dans le tiroir."),
                (E, "Bonjour, le petit pain, s'il te—"),
                (N, "Les pièces tintent. Le mot se casse contre le métal."),
                (N, "Raphaël ouvre la bouche plus fort, puis la referme."),
                (N, "Il refuse de foncer. Il regarde le croissant d'eau, à la vitre."),
                (N, "Une goutte y tremble, sans tomber."),
                (E, "Quand les pièces ont fini, je peux dire ?"),
                (P, "Oui. Le tiroir est fermé. Elle t'écoute."),
                (N, "Un peu de farine colle au sachet, blanc, comme un nuage."),
                (M, "Que veux-tu mettre dans le panier, maintenant ?"),
            ),
            "pieces,farine",
            "croissant d'eau",
        ),
        ("boulangerie", "voisin"): (
            L(
                (N, "Le voisin bloque la porte, panier d'osier contre le ventre."),
                (N, "Il raconte une histoire longue, au sujet d'un pigeon."),
                (E, "Pardon, je veux—"),
                (N, "La phrase du voisin recouvre la sienne, tiède comme le four."),
                (N, "Raphaël sent ses joues chauffer. Il recule d'un pas."),
                (N, "Il pose deux doigts sur l'anse de papa, sans tirer."),
                (E, "Quand son pigeon a fini, je parle ?"),
                (M, "Son pigeon a fini. Nous t'écoutons, et lui aussi."),
                (N, "Le voisin incline la tête. L'anse de son panier craque."),
                (N, "À la vitre, le croissant d'eau garde une goutte ronde."),
                (P, "Que veux-tu demander, maintenant que l'oreille est libre ?"),
            ),
            "porte,panier",
            "anse",
        ),
        ("boulangerie", "maitresse"): (
            L(
                (N, "La maîtresse tient un sac d'école, près des croûtes dorées."),
                (N, "Elle parle à maman d'un dessin, sans voir Raphaël."),
                (E, "Maîtresse, bonjour, je—"),
                (N, "Les deux voix d'adultes se mélangent. Son mot tombe."),
                (N, "Il serre le panier. L'osier pique sa paume."),
                (N, "Il attend que le dessin s'arrête, bouche fermée."),
                (E, "Quand le dessin est rangé, je dis les mots ?"),
                (M, "Le dessin est rangé. Elle se tourne. On t'écoute."),
                (N, "Le sac sent le pain, et un peu de crayon."),
                (N, "Le croissant d'eau, dehors, fait une virgule sombre."),
                (P, "Que veux-tu lui demander, maintenant ?"),
            ),
            "sac,pain",
            "dessin",
        ),
        ("etal", "boulangere"): (
            L(
                (N, "La boulangère est sortie, tablier blanc, loin du four."),
                (N, "Elle pèse des pommes, les yeux sur la balance."),
                (E, "Bonjour, j'aimerais—"),
                (N, "L'aiguille de la balance tremble. Elle n'entend pas."),
                (N, "Un papier vert claque au vent, au-dessus des caisses."),
                (N, "Raphaël avale son envie de crier plus fort."),
                (E, "Quand l'aiguille s'arrête, je peux parler ?"),
                (P, "Elle s'arrête. La boulangère lève les yeux. Vas-y."),
                (N, "Sous le store, le croissant d'eau brille, plus sombre."),
                (N, "Une miette roule près du pied de Raphaël."),
                (M, "Que veux-tu mettre dans l'osier, à présent ?"),
            ),
            "balance,papier",
            "aiguille",
        ),
        ("etal", "voisin"): (
            L(
                (N, "Le voisin a posé son panier en travers de l'étal."),
                (N, "Il discute du prix, d'une voix ronde, trop large."),
                (E, "S'il te plaît, je voudrais—"),
                (N, "Le prix recouvre le mot. Le papier vert claque."),
                (N, "Raphaël recule. Son ventre se serre, sous l'écharpe."),
                (N, "Il regarde le croissant d'eau, au-dessus des caisses."),
                (E, "Quand le prix est dit, je passe ?"),
                (M, "Le prix est dit. Son panier se décale. On t'écoute."),
                (N, "L'osier du voisin frotte le bois mouillé, un bruit sec."),
                (N, "Le pigeon saute plus loin, miette oubliée."),
                (P, "Que veux-tu demander, maintenant que le chemin est libre ?"),
            ),
            "prix,osier",
            "croissant d'eau",
        ),
        ("etal", "maitresse"): (
            L(
                (N, "La maîtresse choisit une feuille de salade, très lente."),
                (N, "Maman lui parle d'un cartable, à voix basse."),
                (E, "Bonjour, maîtresse, le—"),
                (N, "Le mot se perd entre la salade et le cartable."),
                (N, "Raphaël touche le coude de maman, puis attend."),
                (N, "Il ne coupe plus. Le papier vert s'immobilise."),
                (E, "Quand la feuille est choisie, je dis les mots ?"),
                (M, "Elle est choisie. Elle te regarde. Nous aussi."),
                (N, "Le sac d'école penche. Une gomme y fait un coin."),
                (N, "Le croissant d'eau, au-dessus, garde sa forme de lune."),
                (P, "Que veux-tu mettre dans le panier, sous le store ?"),
            ),
            "salade,cartable",
            "feuille",
        ),
        ("fromagerie", "boulangere"): (
            L(
                (N, "La boulangère est entrée, loin du four, pour un peu de lait."),
                (N, "Elle parle au marbre, du fromage à tartiner."),
                (E, "Bonjour, je peux—"),
                (N, "Le mot glisse sur le marbre froid, sans oreille."),
                (N, "Raphaël sent le froid aux doigts. Il se tait."),
                (N, "À la porte, le croissant d'eau fait une virgule."),
                (E, "Quand le lait est dit, je parle ?"),
                (P, "Le lait est dit. Elle se tourne. Tes mots ont de la place."),
                (N, "Un papier blanc attend, plié, près de la balance."),
                (N, "La farine de son tablier fait un nuage, dans l'air frais."),
                (M, "Que veux-tu demander, sur ce marbre froid ?"),
            ),
            "marbre,lait",
            "lait",
        ),
        ("fromagerie", "voisin"): (
            L(
                (N, "Le voisin appuie son panier sur le comptoir de marbre."),
                (N, "Il raconte un fromage d'hier, trop fort, trop long."),
                (E, "Pardon, s'il te plaît—"),
                (N, "Le récit d'hier recouvre sa phrase. Raphaël serre les dents."),
                (N, "Il recule le panier troué. Il refuse de crier."),
                (N, "Il fixe le croissant d'eau, collé à la vitre froide."),
                (E, "Quand hier est fini, je dis les mots d'à présent ?"),
                (M, "Hier est fini. Le marbre t'écoute. Nous aussi."),
                (N, "Le voisin décale l'osier. Un rond d'eau reste sur le blanc."),
                (N, "Ça sent le lait, et un peu de cave."),
                (P, "Que veux-tu mettre dans le trou du panier ?"),
            ),
            "marbre,fromage",
            "vitre froide",
        ),
        ("fromagerie", "maitresse"): (
            L(
                (N, "La maîtresse commande un petit fromage, pour le goûter."),
                (N, "Elle parle à maman d'une chanson, près du marbre."),
                (E, "Maîtresse, merci, je—"),
                (N, "La chanson et la commande se mélangent. Rien n'arrive."),
                (N, "Raphaël pose le panier à terre, pour ne plus bouger."),
                (N, "Il attend que la chanson se ferme, comme une porte."),
                (E, "Quand la chanson est finie, je peux dire ?"),
                (P, "Elle est finie. Elle te regarde. Vas-y, tout entier."),
                (N, "Le sac d'école sent le fromage, un instant, bizarre."),
                (N, "Le croissant d'eau, à la porte, ne tombe pas."),
                (M, "Que veux-tu demander, maintenant que c'est ton tour ?"),
            ),
            "chanson,marbre",
            "chanson",
        ),
    }


def t3_scenes() -> dict:
    data: dict = {}

    def S(*rows):
        return L(*rows)

    # --- BOULANGERIE + BOULANGÈRE ---
    data[("boulangerie", "boulangere", "pain")] = (
        S(
            (N, "Raphaël montre le petit pain, derrière la vitre chaude."),
            (N, "Il ouvre la bouche trop tôt. La cloche fait ding."),
            (E, "Attends. Pas maintenant."),
            (N, "Il regarde le croissant d'eau, collé à la vitre."),
            (N, "La goutte part. Toc, sur le seuil."),
            (E, "Bonjour. S'il te plaît, le petit pain. Merci."),
            (N, "La boulangère hoche. Le sachet papier craque, tiède."),
            (P, "Toute la phrase est arrivée. Tu l'as entendue ?"),
            (M, "Oui. Les trois mots, et le pain."),
            (N, "Un peu de farine tombe dans le trou du panier."),
        ),
        S(
            (N, "Ils reviennent sous la toile rayée, pain contre l'osier."),
            (N, "La croûte chauffe le trou, comme une petite lampe."),
            (M, "Le moment difficile, tu le gardes où ?"),
            (E, "Quand la cloche a parlé trop fort."),
            (E, "J'ai regardé le croissant, puis j'ai dit merci."),
            (P, "On a eu les trois mots, sans morceau perdu."),
            (N, "Le croissant d'eau a laissé une rayure plus sombre."),
            (N, "Une goutte tremble, puis choisit le pavé, pas la chaussure."),
            (N, "Raphaël pose deux doigts sur l'anse rêche."),
            (N, "La farine du trou fait un croissant minuscule, à elle."),
            (N, "Le pigeon a changé de miette, plus loin."),
            (N, "Le store se tait, un moment, comme une oreille."),
        ),
        "sachet,pain",
        "store,goutte",
        "petit pain",
    )
    data[("boulangerie", "boulangere", "pomme")] = (
        S(
            (N, "Près des croûtes, une pomme rouge attend dans une caisse."),
            (N, "Raphaël parle pendant que la boulangère essuie la vitre."),
            (N, "Le chiffon frotte. Son mot glisse."),
            (E, "Je n'aime pas ça. J'attends le toc."),
            (N, "Le croissant d'eau lâche sa goutte. Silence."),
            (E, "Bonjour. S'il te plaît, la pomme. Merci."),
            (N, "Elle la pose. Un point jaune brille sur la peau."),
            (M, "Le chiffon s'est tu. Tes mots, non."),
            (P, "La pomme est à toi, entière, comme la phrase."),
            (N, "Le point jaune s'aligne avec le trou du panier."),
        ),
        S(
            (N, "Sous le store, la pomme roule un peu, puis s'arrête."),
            (N, "Le point jaune regarde le croissant d'eau, au-dessus."),
            (M, "Tu raconteras le chiffon, ou le toc ?"),
            (E, "Le toc. Après, elle m'a vue."),
            (P, "Nous aussi. Toute la pomme, toute la phrase."),
            (N, "L'écharpe rouge frotte la peau lisse, un peu froide."),
            (N, "Une goutte part du croissant, et manque la chaussure."),
            (N, "Raphaël rit, bas, sans crier sur le marché."),
            (N, "Le trou de l'osier cadre le point jaune, un œil."),
            (N, "Ça sent le pain, et un peu de pluie arrêtée."),
            (N, "Papa cale le panier contre sa hanche, sans parler."),
            (N, "La toile rayée garde sa virgule sombre, souvenir."),
        ),
        "pomme,vitre",
        "store,pomme",
        "point jaune",
    )
    data[("boulangerie", "boulangere", "fromage")] = (
        S(
            (N, "Un fromage en papier blanc attend, près des brioches."),
            (N, "Raphaël commence. Elle coupe une tranche, plus loin."),
            (N, "Le couteau parle. Lui, non."),
            (E, "Quand le couteau dort, je dis."),
            (N, "Il suit le croissant d'eau. Toc. Le couteau s'arrête."),
            (E, "Bonjour. S'il te plaît, le fromage. Merci."),
            (N, "Elle tend le paquet. Ça sent le lait, dans le beurre."),
            (P, "Le couteau a eu son tour. Toi, le tien."),
            (M, "Le papier blanc se tait, dans tes mains."),
            (N, "Un coin du papier passe dans le trou, comme un drapeau."),
        ),
        S(
            (N, "Ils marchent sous le store. Le fromage pèse, frais."),
            (N, "Le drapeau de papier clignote dans le trou d'osier."),
            (M, "Le difficile, c'était le couteau, ou ta bouche ?"),
            (E, "Ma bouche. Elle voulait couper, elle aussi."),
            (E, "J'ai attendu le toc. Après, merci."),
            (P, "On a entendu le merci, entier."),
            (N, "Le croissant d'eau s'affine, presque une rayure."),
            (N, "Raphaël touche le papier, puis l'anse, deux textures."),
            (N, "Une goutte choisit une caisse, pas sa chaussure."),
            (N, "Le four, derrière, souffle moins fort."),
            (N, "Maman noue plus serré l'écharpe, sans leçon."),
            (N, "Le marché reprend, mais sa phrase reste posée."),
        ),
        "fromage,papier",
        "store,papier",
        "drapeau",
    )

    # --- BOULANGERIE + VOISIN ---
    data[("boulangerie", "voisin", "pain")] = (
        S(
            (N, "Le voisin tient le petit pain, par hasard, dans sa main."),
            (N, "Raphaël le lui demande pendant l'histoire du pigeon."),
            (N, "Le pigeon du récit s'envole. Le pain, non."),
            (E, "Je ne coupe plus. Je regarde la goutte."),
            (N, "Le croissant d'eau lâche. Toc. Le voisin se tait."),
            (E, "Bonjour. S'il te plaît, ce pain. Merci."),
            (N, "Le voisin le pose dans l'osier, un peu étonné."),
            (P, "Ton pigeon a fini. Son pain commence."),
            (M, "Les trois mots ont trouvé une anse, la sienne."),
            (N, "La croûte laisse une miette dans le trou du fond."),
        ),
        S(
            (N, "Sous la toile, la miette du trou ne tombe pas."),
            (N, "Elle reste, coincée, comme le mot d'avant."),
            (M, "Tu as laissé le pigeon finir, cette fois."),
            (E, "Oui. Après, le pain m'a écouté."),
            (P, "Le voisin aussi. Toute la phrase, sans aile."),
            (N, "Raphaël souffle sur la miette. Elle tient."),
            (N, "Le croissant d'eau a séché d'un bord, pas de l'autre."),
            (N, "Une goutte part, tardive, et tape le pavé."),
            (N, "Sa chaussure reste sèche. Ça lui va."),
            (N, "L'anse rêche chauffe, à force d'être tenue."),
            (N, "Le four sent moins. Le store sent le bois mouillé."),
            (N, "Ils s'éloignent. Le pigeon vrai picore ailleurs."),
        ),
        "pain,pigeon",
        "miette,store",
        "miette",
    )
    data[("boulangerie", "voisin", "pomme")] = (
        S(
            (N, "Une pomme a roulé près du panier du voisin."),
            (N, "Raphaël parle. Le voisin la ramasse en même temps."),
            (N, "Deux gestes. Un mot perdu."),
            (E, "Toi d'abord, la pomme. Après, moi."),
            (N, "Il attend le toc du croissant d'eau, à la porte."),
            (E, "Bonjour. S'il te plaît, la pomme. Merci."),
            (N, "Le voisin la tend. Un point jaune vers Raphaël."),
            (M, "Tu as laissé sa main finir. La tienne a parlé."),
            (P, "La pomme n'a pas coupé tes mots."),
            (N, "Elle se cale contre l'osier, froide, ronde."),
        ),
        S(
            (N, "Le point jaune voyage sous le store, dans le panier."),
            (N, "Il passe devant le trou, puis revient, un œil."),
            (M, "Le difficile, c'était sa main, ou ta voix ?"),
            (E, "Sa main. J'ai dit : toi d'abord."),
            (P, "Et le toc a dit : maintenant, toi."),
            (N, "Raphaël appuie l'écharpe contre la pomme, un instant."),
            (N, "Le croissant d'eau s'est aminci, virgule plus pâle."),
            (N, "Une goutte manque le pigeon, et rit presque."),
            (N, "Papa décale le panier. Rien ne tombe."),
            (N, "La porte de la boulangerie se ferme, cloche muette."),
            (N, "Raphaël garde le silence, cette fois par choix."),
            (N, "Le marché a de la place, autour de sa phrase."),
        ),
        "pomme,voisin",
        "store,pomme",
        "point jaune",
    )
    data[("boulangerie", "voisin", "fromage")] = (
        S(
            (N, "Le fromage en papier est coincé sous l'anse du voisin."),
            (N, "Raphaël tire trop tôt. Le papier crie."),
            (E, "Pas tirer. Attendre le toc."),
            (N, "Le croissant d'eau lâche sa goutte. Le papier se tait."),
            (E, "Bonjour. S'il te plaît, le fromage. Merci."),
            (N, "Le voisin libère le paquet, un peu gêné, gentiment."),
            (P, "L'anse a eu son tour. Le papier, le tien."),
            (M, "On a entendu merci, sans le cri du papier."),
            (N, "Ça sent le lait, près du beurre chaud, bizarre et bon."),
            (N, "Un coin blanc dépasse du trou, petit drapeau."),
        ),
        S(
            (N, "Sous le store, le drapeau de papier cligne, puis s'immobilise."),
            (N, "Raphaël ne le rentre pas. Il le laisse respirer."),
            (M, "Tu as failli tirer. Tu as regardé la goutte."),
            (E, "Oui. Le papier a crié. Moi, non."),
            (P, "Tes mots, eux, sont arrivés propres."),
            (N, "Le croissant d'eau a une bordure plus nette, comme un dessin."),
            (N, "Une goutte part vers une caisse, pas vers la chaussure."),
            (N, "L'osier sent le lait, un instant, puis le bois."),
            (N, "Le voisin disparaît vers un autre étal, histoire finie."),
            (N, "Raphaël pose la paume sur le paquet, sans parler."),
            (N, "Maman ajuste l'écharpe. Le rouge tient chaud."),
            (N, "Le store écoute, rayure après rayure."),
        ),
        "fromage,papier",
        "drapeau,store",
        "papier",
    )

    # --- BOULANGERIE + MAÎTRESSE ---
    data[("boulangerie", "maitresse", "pain")] = (
        S(
            (N, "La maîtresse a un petit pain dans le sac d'école, par erreur."),
            (N, "Raphaël le demande pendant qu'elle parle du dessin."),
            (N, "Le dessin recouvre le pain, et les mots."),
            (E, "Le dessin d'abord. Après, le toc. Après, moi."),
            (N, "Le croissant d'eau tombe. Elle se tait."),
            (E, "Bonjour. S'il te plaît, le pain. Merci."),
            (N, "Elle le sort du sac. Il est un peu écrasé, tiède."),
            (M, "Le dessin est fini. Le pain, à toi."),
            (P, "Tes trois mots ont redressé la croûte, un peu."),
            (N, "Une miette d'école tombe dans le trou de l'osier."),
        ),
        S(
            (N, "Sous la toile, le pain écrasé sent plus fort, presque le goûter."),
            (N, "La miette d'école reste dans le trou, comme un secret."),
            (M, "Tu as laissé le dessin. C'était dur ?"),
            (E, "Oui. Mes mots poussaient. Je les ai retenus."),
            (P, "On les a reçus, après le toc, entiers."),
            (N, "Le croissant d'eau a la forme d'un crayon, un instant."),
            (N, "Puis ce n'est plus qu'une tache sombre, sage."),
            (N, "Raphaël ne touche pas le sac. Il tient l'anse."),
            (N, "Une goutte tape le seuil de la boulangerie, loin."),
            (N, "L'écharpe sent le pain, et un peu de craie."),
            (N, "Ils s'éloignent. La cloche, derrière, ne dit plus rien."),
            (N, "Le store a pris le pain, et la phrase, sous son ventre."),
        ),
        "pain,sac",
        "store,miette",
        "miette d'école",
    )
    data[("boulangerie", "maitresse", "pomme")] = (
        S(
            (N, "Une pomme dépasse du sac d'école, rouge, trop visible."),
            (N, "Raphaël la nomme pendant que maman parle du cartable."),
            (N, "Trois voix. Zéro pomme entendue."),
            (E, "Une voix. La mienne, après le toc."),
            (N, "Il fixe le croissant d'eau. La goutte part. Silence."),
            (E, "Bonjour. S'il te plaît, la pomme. Merci."),
            (N, "La maîtresse la tend. Le point jaune vers lui."),
            (P, "Le cartable s'est tu. La pomme a une oreille."),
            (M, "Tes mots ont marché, un par un."),
            (N, "La pomme se loge, ronde, contre le trou, sans tomber."),
        ),
        S(
            (N, "Le point jaune voyage sous le store, un phare minuscule."),
            (N, "Raphaël le montre à papa, sans parler trop vite."),
            (M, "Trois voix, tout à l'heure. Maintenant, une."),
            (E, "La mienne. Après le toc. Merci est arrivé."),
            (P, "On l'a. La pomme aussi."),
            (N, "Le croissant d'eau s'est ouvert, puis refermé, comme une bouche."),
            (N, "Une goutte choisit le pavé. La chaussure reste nette."),
            (N, "Le sac d'école s'éloigne, plus léger d'une pomme."),
            (N, "L'osier sent le fruit froid, et le pain chaud, ensemble."),
            (N, "Raphaël sourit dans l'écharpe, invisible, vrai."),
            (N, "Le pigeon ignore la pomme. Tant mieux."),
            (N, "La toile rayée garde le croissant, plus pâle."),
        ),
        "pomme,sac",
        "store,pomme",
        "phare",
    )
    data[("boulangerie", "maitresse", "fromage")] = (
        S(
            (N, "Le fromage en papier a glissé contre le sac d'école."),
            (N, "Raphaël parle. Une gomme tombe. Tout le monde se baisse."),
            (N, "Les mots se perdent vers le carrelage."),
            (E, "La gomme d'abord. Moi, après le toc."),
            (N, "On ramasse. Le croissant d'eau lâche. Il parle."),
            (E, "Bonjour. S'il te plaît, le fromage. Merci."),
            (N, "Elle lui donne le paquet. La gomme rentre dans le sac."),
            (M, "Deux objets. Un tour chacun. Tes mots, à la fin."),
            (P, "Le marbre n'est pas là. Le carrelage a suffi."),
            (N, "Le papier blanc se tait, coincé, dans le trou."),
        ),
        S(
            (N, "Sous le store, la gomme n'est plus là. Le fromage, si."),
            (N, "Raphaël écoute le papier. Il ne crie plus."),
            (M, "Tu as laissé tomber la gomme, pas tes mots."),
            (E, "Ils ont attendu, par terre, avec nous."),
            (P, "Puis ils se sont levés, propres."),
            (N, "Le croissant d'eau a une goutte unique, ronde, sage."),
            (N, "Elle part. Toc, sur une caisse, pas sur lui."),
            (N, "L'écharpe sent le lait, un instant, puis le pain."),
            (N, "La maîtresse range le sac. Le dessin est ailleurs."),
            (N, "Papa cale le panier. Rien ne fuit par le trou."),
            (N, "Raphaël pose un doigt sur le papier, comme sur une bouche."),
            (N, "Le store, au-dessus, a fini de parler trop fort."),
        ),
        "fromage,gomme",
        "store,gomme",
        "gomme",
    )

    # --- ÉTAL + BOULANGÈRE ---
    data[("etal", "boulangere", "pain")] = (
        S(
            (N, "La boulangère a emporté un petit pain, pour le chemin."),
            (N, "Raphaël le demande. L'aiguille de la balance tremble."),
            (N, "Le pain penche. Les mots aussi."),
            (E, "L'aiguille d'abord. Moi, après le toc."),
            (N, "Le croissant d'eau, au-dessus des caisses, lâche."),
            (E, "Bonjour. S'il te plaît, le pain. Merci."),
            (N, "Elle le pose. Le sachet claque, comme le papier vert."),
            (P, "La balance s'est arrêtée. Tes mots, non : ils tiennent."),
            (M, "Le pain est à l'osier. La phrase, à nous."),
            (N, "Une croûte sème de la farine sur le bois mouillé."),
        ),
        S(
            (N, "Ils restent sous le store. Le pain sent le four, ici, dehors."),
            (N, "La farine du bois fait une trace, puis s'efface."),
            (M, "L'aiguille a tremblé. Toi, non."),
            (E, "J'ai regardé le croissant. Après, merci."),
            (P, "On a le pain, et les trois mots, sans tremblement."),
            (N, "Le croissant d'eau a perdu un bord, plus clair."),
            (N, "Une goutte tape une caisse. Le pigeon s'envole."),
            (N, "Raphaël ne court pas après. Il tient l'anse."),
            (N, "Le papier vert se calme, collé, mouillé d'un côté."),
            (N, "L'écharpe prend l'odeur du pain, et de la pluie."),
            (N, "Papa hausse le panier. Le trou ne lâche rien."),
            (N, "La toile rayée fait un toit, enfin silencieux."),
        ),
        "pain,balance",
        "store,farine",
        "aiguille",
    )
    data[("etal", "boulangere", "pomme")] = (
        S(
            (N, "La boulangère pèse la pomme que Raphaël désigne."),
            (N, "Il parle trop tôt. L'aiguille n'a pas fini."),
            (E, "Chut, moi. Toi, l'aiguille."),
            (N, "Il lève les yeux. Le croissant d'eau lâche sa goutte."),
            (E, "Bonjour. S'il te plaît, cette pomme. Merci."),
            (N, "Elle la pose dans sa paume. Le point jaune vers le ciel."),
            (M, "L'aiguille s'est tue. Tes mots ont un poids, eux aussi."),
            (P, "Un vrai poids, de pomme, et de phrase."),
            (N, "La peau froide mouille un peu le trou de l'osier."),
            (N, "Le papier vert ne claque plus."),
        ),
        S(
            (N, "Sous le store, le point jaune cherche le croissant d'eau."),
            (N, "Ils se répondent, deux formes, sans bruit."),
            (M, "Tu as dit chut à toi-même. C'était nouveau."),
            (E, "Oui. Après le toc, j'ai dit les trois mots."),
            (P, "On les a reçus, avec la pomme, froids et nets."),
            (N, "Une goutte part. Elle manque le point jaune, exprès."),
            (N, "Raphaël essuie la pomme sur l'écharpe, un rond rouge."),
            (N, "Le bois des caisses sent la pluie, et un peu de sucre."),
            (N, "La boulangère rentre vers le four, tablier mouillé d'un coin."),
            (N, "Le panier penche. La pomme tient, contre le trou."),
            (N, "Papa ne parle pas. Il a entendu, c'est assez."),
            (N, "La toile garde une virgule, plus sombre que les rayures."),
        ),
        "pomme,balance",
        "store,pomme",
        "poids",
    )
    data[("etal", "boulangere", "fromage")] = (
        S(
            (N, "Un fromage en papier repose entre deux caisses, trop au frais."),
            (N, "Raphaël le demande. Un papier vert claque au-dessus."),
            (N, "Le claquement mange le merci."),
            (E, "Le papier d'abord. Le toc ensuite. Moi, après."),
            (N, "Le croissant d'eau tombe. Le vert s'immobilise."),
            (E, "Bonjour. S'il te plaît, le fromage. Merci."),
            (N, "La boulangère le glisse. Le blanc contre le bois mouillé."),
            (P, "Le claquement a fini. Tes mots, eux, restent."),
            (M, "Le fromage a froid. Ta phrase, non."),
            (N, "Un coin de papier boit une goutte, dans le trou."),
        ),
        S(
            (N, "Ils s'éloignent un peu, sans quitter le store."),
            (N, "Le papier blanc a une tache ronde, souvenir d'eau."),
            (M, "Le vert a claqué. Toi, tu as attendu."),
            (E, "Oui. Merci est parti après le toc, pas pendant."),
            (P, "On l'a, entier, avec le fromage froid."),
            (N, "Le croissant d'eau s'est refermé, plus petit, plus net."),
            (N, "Une goutte choisit le papier vert, plus loin, pas eux."),
            (N, "Raphaël palpe le paquet. Ça sent la cave, sous la pluie."),
            (N, "L'anse rêche gratte. Il ne lâche pas."),
            (N, "Le pigeon revient, miette nouvelle, sans les déranger."),
            (N, "Maman recouvre le fromage d'un coin d'écharpe, un toit."),
            (N, "La toile rayée a deux papiers, un vert, un blanc, et le calme."),
        ),
        "fromage,papier",
        "store,tache",
        "tache ronde",
    )

    # --- ÉTAL + VOISIN ---
    data[("etal", "voisin", "pain")] = (
        S(
            (N, "Le pain du voisin dépasse de son osier, croûte au vent."),
            (N, "Raphaël le demande pendant le prix des pommes."),
            (N, "Le prix est trop large. Le pain n'entend rien."),
            (E, "Le prix d'abord. Le toc. Puis moi."),
            (N, "Le croissant d'eau lâche, au-dessus des caisses."),
            (E, "Bonjour. S'il te plaît, un pain. Merci."),
            (N, "Le voisin en tend un, plus petit, à lui."),
            (M, "Le prix s'est tu. Le pain a changé de panier."),
            (P, "Tes mots ont payé, sans pièces."),
            (N, "La croûte sème une miette, qui reste dans le trou."),
        ),
        S(
            (N, "Sous le store, deux paniers d'osier se ressemblent, un instant."),
            (N, "Puis le petit pain distingue celui de Raphaël."),
            (M, "Tu as laissé le prix. C'était long."),
            (E, "Long. Après le toc, merci a suffi."),
            (P, "Suffi pour nous. Suffi pour le pain."),
            (N, "Le croissant d'eau a une brillance courte, puis s'apaise."),
            (N, "Une goutte tape l'osier du voisin, pas le leur."),
            (N, "Raphaël rit de ce toc-là, différent, plus loin."),
            (N, "Le papier vert se colle, mouillé, à une caisse."),
            (N, "L'écharpe sent le four, dehors, comme un secret."),
            (N, "Papa hausse les deux anses. Rien ne tombe."),
            (N, "Le marché reprend ses prix. Leur phrase, elle, est payée."),
        ),
        "pain,prix",
        "deux-paniers,store",
        "petit pain",
    )
    data[("etal", "voisin", "pomme")] = (
        S(
            (N, "Le voisin a la pomme dans la main, pour la peser."),
            (N, "Raphaël parle. L'homme discute du prix, sans lâcher."),
            (N, "La pomme tourne. Les mots, non."),
            (E, "Quand elle ne tourne plus, je dis."),
            (N, "Il attend le croissant d'eau. Toc. La pomme s'arrête."),
            (E, "Bonjour. S'il te plaît, cette pomme. Merci."),
            (N, "Le voisin la pose. Le point jaune vers Raphaël."),
            (P, "Elle a fini de tourner. Tes mots, eux, tiennent."),
            (M, "Le prix peut attendre. La pomme, non."),
            (N, "Elle se cale, froide, pile au-dessus du trou."),
        ),
        S(
            (N, "Le point jaune, sous le store, ne tourne plus."),
            (N, "Il fixe le croissant d'eau, deux ronds, l'un pâle, l'un sombre."),
            (M, "Tu as regardé la pomme s'arrêter. Puis le toc."),
            (E, "Puis les trois mots. Merci en dernier."),
            (P, "En dernier, et entier. On l'a."),
            (N, "Une goutte part du croissant, et évite le point jaune."),
            (N, "Raphaël souffle dessus, pour rire, sans la mouiller."),
            (N, "Le voisin reprend son prix, plus loin, plus bas."),
            (N, "L'osier sent le fruit, et le bois mouillé des caisses."),
            (N, "L'écharpe fait un nid, un instant, autour de la pomme."),
            (N, "Papa ne pèse rien. Il a compris le poids des mots."),
            (N, "La toile rayée tient le croissant, comme une balance."),
        ),
        "pomme,prix",
        "store,point",
        "pomme",
    )
    data[("etal", "voisin", "fromage")] = (
        S(
            (N, "Le fromage du voisin dépasse, papier taché d'une goutte."),
            (N, "Raphaël le demande. L'homme recule le panier, trop vite."),
            (N, "Les deux osiers se cognent. Les mots se cognent aussi."),
            (E, "Les paniers d'abord. Moi, après le toc."),
            (N, "Le croissant d'eau tombe. Les anses s'écartent."),
            (E, "Bonjour. S'il te plaît, un fromage. Merci."),
            (N, "Le voisin en tend un, propre, papier net."),
            (M, "Les paniers ont fini de se battre. Tes mots, non."),
            (P, "Ils se sont posés, comme le papier blanc."),
            (N, "Le paquet neuf entre dans le trou, juste, sans forcer."),
        ),
        S(
            (N, "Sous le store, deux papiers : un taché, loin, un net, ici."),
            (N, "Raphaël garde le net, sans se moquer de l'autre."),
            (M, "Les osiers se sont cognés. Toi, tu as reculé."),
            (E, "Oui. Après le toc, j'ai dit merci, propre."),
            (P, "Propre, on l'a entendu. Le fromage aussi."),
            (N, "Le croissant d'eau a une tache jumelle, plus haute."),
            (N, "Une goutte part, et manque les deux paniers."),
            (N, "Raphaël palpe le papier. Ça sent le lait, et la pluie."),
            (N, "Le voisin part, anse craquante, histoire ailleurs."),
            (N, "Le papier vert se tait. Le blanc aussi."),
            (N, "Papa cale le fond. Le trou ne lâche pas le paquet."),
            (N, "La toile rayée a cessé de claquer, comme une joue."),
        ),
        "fromage,choc",
        "store,papier",
        "papier net",
    )

    # --- ÉTAL + MAÎTRESSE ---
    data[("etal", "maitresse", "pain")] = (
        S(
            (N, "La maîtresse a acheté un pain, trop grand pour le sac."),
            (N, "Raphaël en veut un, plus petit. Il parle trop tôt."),
            (N, "Le sac refuse. Les mots aussi, coincés."),
            (E, "Le sac d'abord. Le toc. Puis le petit."),
            (N, "Le croissant d'eau lâche. Le sac s'ouvre d'un cran."),
            (E, "Bonjour. S'il te plaît, un petit pain. Merci."),
            (N, "Elle lui en passe un, à côté, sachet à part."),
            (P, "Le grand a son sac. Le petit, tes mots."),
            (M, "Les trois mots ont trouvé un pain à leur taille."),
            (N, "Une miette tombe, et reste dans le trou, comme à l'école."),
        ),
        S(
            (N, "Sous le store, le petit pain chauffe l'osier, juste assez."),
            (N, "La miette du trou ne tombe pas sur le pavé."),
            (M, "Le sac était trop plein. Ta phrase, non."),
            (E, "J'ai attendu le cran. Après, merci."),
            (P, "On a le petit, et les trois mots, sans coincer."),
            (N, "Le croissant d'eau s'est ouvert d'un cran, lui aussi."),
            (N, "Une goutte part, lente, vers une feuille de salade."),
            (N, "Raphaël ne la suit pas. Il tient le sachet."),
            (N, "L'écharpe sent le four, et un peu de gomme, bizarre."),
            (N, "La maîtresse rentre le grand pain. Le sac accepte."),
            (N, "Papa hausse l'anse. Le trou garde la miette."),
            (N, "La toile rayée fait un préau, un instant, puis redevient store."),
        ),
        "pain,sac",
        "store,petit-pain",
        "petit pain",
    )
    data[("etal", "maitresse", "pomme")] = (
        S(
            (N, "La maîtresse tient une pomme, et une feuille, trop d'un coup."),
            (N, "Raphaël demande la pomme. La feuille glisse."),
            (N, "Tout le monde se baisse. Les mots se baissent aussi."),
            (E, "La feuille d'abord. Moi, après le toc."),
            (N, "On ramasse. Le croissant d'eau tombe. Silence."),
            (E, "Bonjour. S'il te plaît, la pomme. Merci."),
            (N, "Elle la tend. Le point jaune a un peu de terre."),
            (M, "La feuille est sauvée. Tes mots aussi."),
            (P, "La pomme a de la terre. La phrase, non."),
            (N, "Il l'essuie sur l'osier. Le trou avale un grain."),
        ),
        S(
            (N, "Sous le store, le grain de terre reste dans le trou, secret."),
            (N, "Le point jaune, lui, est propre, vers le croissant d'eau."),
            (M, "Tu t'es baissé pour la feuille, pas pour crier."),
            (E, "Après, le toc. Après, les trois mots."),
            (P, "On les a, propres, comme le point jaune."),
            (N, "Une goutte part du croissant, et lave le pavé, pas la pomme."),
            (N, "Raphaël la fait tourner, lente, sans parler."),
            (N, "La feuille de salade brille, plus loin, dans un autre sac."),
            (N, "L'écharpe a un peu de terre, un peu de rouge."),
            (N, "Papa souffle le grain, sans vider le panier."),
            (N, "Le pigeon ignore le grain. Il a sa miette."),
            (N, "La toile rayée tient le croissant, plus net après la goutte."),
        ),
        "pomme,feuille",
        "store,grain",
        "grain",
    )
    data[("etal", "maitresse", "fromage")] = (
        S(
            (N, "Le fromage de la maîtresse dépasse du sac, papier trop long."),
            (N, "Raphaël le demande. Une gomme tombe, entre les caisses."),
            (N, "Le toc de la gomme n'est pas le bon toc."),
            (E, "Pas cette gomme. Le croissant, lui."),
            (N, "Il lève les yeux. La vraie goutte part. Silence."),
            (E, "Bonjour. S'il te plaît, le fromage. Merci."),
            (N, "Elle lui en passe un, plus petit, papier court."),
            (P, "Deux tocs. Tu as choisi le bon."),
            (M, "Le fromage court a tes mots, entiers."),
            (N, "Le papier court rentre dans le trou, sans dépasser."),
        ),
        S(
            (N, "Sous le store, le papier court ne claque pas, contrairement au vert."),
            (N, "Raphaël l'écoute. Rien. Ça lui va."),
            (M, "La gomme a tapé. Tu as regardé plus haut."),
            (E, "Le croissant. Le vrai toc. Puis merci."),
            (P, "On a le vrai, et le fromage, et la phrase."),
            (N, "Le croissant d'eau a deux bords, comme deux tocs, l'un pâle."),
            (N, "Une goutte choisit le pavé. La gomme, elle, est ramassée."),
            (N, "L'osier sent le lait, et le bois, et un peu de caoutchouc."),
            (N, "Raphaël rit de ce mélange, bas, dans l'écharpe."),
            (N, "La maîtresse ferme le sac. Plus rien ne tombe."),
            (N, "Papa cale le fond. Le papier court tient."),
            (N, "La toile rayée a repris son vrai bruit, le goutte-à-goutte."),
        ),
        "fromage,gomme",
        "store,toc",
        "vrai toc",
    )

    # --- FROMAGERIE + BOULANGÈRE ---
    data[("fromagerie", "boulangere", "pain")] = (
        S(
            (N, "La boulangère a posé son pain sur le marbre, le temps du lait."),
            (N, "Raphaël le demande. Elle parle tartine, sans le voir."),
            (N, "Le marbre froid avale les mots, comme le lait."),
            (E, "La tartine d'abord. Le toc. Puis moi."),
            (N, "À la porte, le croissant d'eau lâche. Elle se tait."),
            (E, "Bonjour. S'il te plaît, le pain. Merci."),
            (N, "Elle le pousse. Tiède sur le marbre, une surprise."),
            (P, "Le lait a eu son tour. Le pain, tes mots."),
            (M, "Chaud et froid, ensemble. Ta phrase, nette."),
            (N, "Une miette fond un peu, puis reste dans le trou."),
        ),
        S(
            (N, "Ils sortent. Le pain tiède fume, sous le store goutteux."),
            (N, "La miette du trou a pris le froid du marbre, un instant."),
            (M, "Tu as laissé la tartine. Puis tu as parlé."),
            (E, "Après le toc de la porte. Merci, à la fin."),
            (P, "On a le pain, et le froid, et les trois mots."),
            (N, "Le croissant d'eau, dehors, est plus large qu'à la vitre."),
            (N, "Une goutte part, et manque la vapeur du pain."),
            (N, "Raphaël cache le pain sous l'écharpe, un nid chaud."),
            (N, "Ça sent le four, et la cave, mélangés, drôles."),
            (N, "La boulangère rentre vers son lait. Le marbre redevient blanc."),
            (N, "Papa hausse l'osier. Rien ne glisse."),
            (N, "Le store reprend le pain, comme un four plus grand, plus lent."),
        ),
        "pain,marbre",
        "store,vapeur",
        "vapeur",
    )
    data[("fromagerie", "boulangere", "pomme")] = (
        S(
            (N, "Une pomme a suivi la boulangère, oubliée, sur le marbre."),
            (N, "Raphaël la demande. Elle essuie le blanc, chiffon large."),
            (N, "Le chiffon recouvre le point jaune, et sa voix."),
            (E, "Le chiffon d'abord. Moi, après le toc."),
            (N, "Le croissant d'eau, à la porte, lâche. Le chiffon s'arrête."),
            (E, "Bonjour. S'il te plaît, la pomme. Merci."),
            (N, "Elle la découvre. Le point jaune a un peu de blanc."),
            (M, "Le marbre est propre. Tes mots aussi."),
            (P, "La pomme a du froid. La phrase, de la place."),
            (N, "Elle entre dans l'osier, et refroidit le trou."),
        ),
        S(
            (N, "Sous le store, le point jaune a gardé une trace de marbre."),
            (N, "Un croissant pâle, sur la peau, répond à celui de la toile."),
            (M, "Deux croissants, maintenant. Tu les vois ?"),
            (E, "Oui. J'ai attendu le vrai, en haut, pour parler."),
            (P, "Et la pomme a le petit, en bas. Tes mots, au milieu."),
            (N, "Une goutte part du haut, et évite le bas, exprès."),
            (N, "Raphaël essuie le blanc sur l'écharpe, un nuage."),
            (N, "Ça sent le lait, et le fruit, et la pluie."),
            (N, "La boulangère rentre, chiffon à la main, loin."),
            (N, "Papa cale la pomme. Le trou ne la boit pas."),
            (N, "Le pigeon, dehors, n'aime pas le fromage. Tant mieux."),
            (N, "La toile rayée tient les deux croissants, le temps d'un silence."),
        ),
        "pomme,chiffon",
        "store,deux-croissants",
        "croissant pâle",
    )
    data[("fromagerie", "boulangere", "fromage")] = (
        S(
            (N, "Le fromage que Raphaël veut est celui de la boulangère, presque."),
            (N, "Il parle. Elle dit : celui-ci, pour les tartines."),
            (N, "Deux fromages. Une seule oreille, pas la sienne."),
            (E, "Le sien d'abord. Le toc. Puis le mien."),
            (N, "Le croissant d'eau tombe. Elle pousse l'autre paquet."),
            (E, "Bonjour. S'il te plaît, celui-là. Merci."),
            (N, "Elle le lui donne. Papier plus épais, odeur plus forte."),
            (P, "Deux fromages. Deux tours. Tes mots, au second."),
            (M, "Le papier épais se tait. On t'a entendu."),
            (N, "Il rentre dans le trou, juste, comme s'il l'attendait."),
        ),
        S(
            (N, "Sous le store, le papier épais ne claque pas. Il pèse."),
            (N, "Raphaël le sent. Cave, lait, et un peu de four."),
            (M, "Tu as laissé les tartines. Puis tu as demandé le tien."),
            (E, "Après le toc. Merci, pour celui-là."),
            (P, "Celui-là, on l'a. Les trois mots aussi."),
            (N, "Le croissant d'eau s'est épaissi, lui aussi, plus sombre."),
            (N, "Une goutte part, lourde, et tape une caisse."),
            (N, "La chaussure de Raphaël reste sèche, cette fois-ci."),
            (N, "Il souffle, content, sans trop le montrer."),
            (N, "L'anse rêche tient. Le trou tient. La phrase tient."),
            (N, "La boulangère disparaît, tartines ailleurs."),
            (N, "Le store, au-dessus, a le poids d'un vrai toit."),
        ),
        "fromage,tartine",
        "store,papier",
        "papier épais",
    )

    # --- FROMAGERIE + VOISIN ---
    data[("fromagerie", "voisin", "pain")] = (
        S(
            (N, "Le voisin a posé son pain sur le marbre, croûte au froid."),
            (N, "Raphaël le demande pendant le fromage d'hier."),
            (N, "Hier est trop long. Le pain refroidit. Les mots aussi."),
            (E, "Hier d'abord. Le toc. Puis à présent, moi."),
            (N, "Le croissant d'eau, à la vitre, lâche. Hier se tait."),
            (E, "Bonjour. S'il te plaît, le pain. Merci."),
            (N, "Le voisin le pousse. La croûte a pris le marbre, un peu."),
            (M, "Hier a fini. Ton pain, c'est maintenant."),
            (P, "Tes mots n'ont pas d'hier. Ils sont là."),
            (N, "Une miette froide reste dans le trou, comme un galet."),
        ),
        S(
            (N, "Sous le store, la miette froide réchauffe, lentement, dans l'osier."),
            (N, "Raphaël la sent du doigt, sans la manger."),
            (M, "Tu as laissé hier. C'était une longue oreille."),
            (E, "Longue. Après le toc, merci a été court."),
            (P, "Court, et entier. On l'a."),
            (N, "Le croissant d'eau a une forme d'hier, puis s'arrondit."),
            (N, "Une goutte d'à présent tape le pavé."),
            (N, "Le pain sous l'écharpe reprend un peu de four, imaginaire."),
            (N, "Le voisin reprend son fromage d'hier, plus loin."),
            (N, "Papa hausse le panier. Le galet de miette tient."),
            (N, "Ça sent le froid, et le chaud, collés."),
            (N, "La toile rayée a oublié hier. Elle goutte, seulement."),
        ),
        "pain,hier",
        "store,miette",
        "miette froide",
    )
    data[("fromagerie", "voisin", "pomme")] = (
        S(
            (N, "Une pomme a roulé sous le panier du voisin, contre le marbre."),
            (N, "Raphaël se baisse et parle, en même temps."),
            (N, "Le marbre rend un écho. Personne n'écoute l'écho."),
            (E, "Je me lève. J'attends le toc. Après, les mots."),
            (N, "Le croissant d'eau tombe. Il se redresse."),
            (E, "Bonjour. S'il te plaît, la pomme. Merci."),
            (N, "Le voisin la dégage. Le point jaune a une poussière blanche."),
            (P, "L'écho s'est tu. Tes mots, à hauteur d'oreille."),
            (M, "La pomme du sol a une phrase, maintenant."),
            (N, "Elle rentre, ronde, et pousse un peu le fond troué."),
        ),
        S(
            (N, "Sous le store, la poussière blanche du point jaune s'en va."),
            (N, "Raphaël souffle. Le jaune regarde le croissant d'eau."),
            (M, "Tu t'es levé pour parler. C'était juste."),
            (E, "Oui. Par terre, les mots restaient par terre."),
            (P, "Debout, après le toc, on les a."),
            (N, "Une goutte part, et n'atteint pas la pomme sauvée."),
            (N, "L'osier sent le marbre, un peu, puis le fruit."),
            (N, "Le voisin recule son panier. Le marbre redevient un lac."),
            (N, "L'écharpe essuie le dernier blanc, un nuage."),
            (N, "Papa ne se baisse plus. Il a entendu, debout."),
            (N, "Le pigeon, dehors, n'a pas de pomme. Il a sa miette."),
            (N, "Le store tient le croissant, à hauteur d'œil, cette fois."),
        ),
        "pomme,echo",
        "store,debout",
        "écho",
    )
    data[("fromagerie", "voisin", "fromage")] = (
        S(
            (N, "Le fromage d'hier du voisin ressemble à celui d'à présent."),
            (N, "Raphaël se trompe, et parle trop tôt, vers le faux."),
            (N, "Le voisin dit non, trop fort. Les mots reculent."),
            (E, "Le faux d'abord. Le toc. Puis le vrai, moi."),
            (N, "Le croissant d'eau lâche. Un vrai paquet avance."),
            (E, "Bonjour. S'il te plaît, celui-là. Merci."),
            (N, "Le voisin le pousse. Papier plus clair, odeur plus nette."),
            (M, "Deux fromages. Tu as choisi après le silence."),
            (P, "Tes mots ont trouvé le vrai, pas hier."),
            (N, "Le papier clair rentre dans le trou, sans se déchirer."),
        ),
        S(
            (N, "Sous le store, le papier clair ne raconte pas hier."),
            (N, "Il sent le présent, net, sans histoire d'hier."),
            (M, "Tu t'es trompé, puis tu as attendu le toc."),
            (E, "Le vrai. Merci, pour celui-là, pas l'autre."),
            (P, "Celui-là, on l'a. Les trois mots aussi, vrais."),
            (N, "Le croissant d'eau a deux lobes, puis n'en garde qu'un."),
            (N, "Une goutte part, et choisit une caisse, pas le papier."),
            (N, "Raphaël palpe. Cave nette, pas cave d'hier."),
            (N, "Le voisin emporte son hier, anse craquante."),
            (N, "L'anse de Raphaël, elle, est rêche et présente."),
            (N, "Papa cale le fond. Le vrai tient."),
            (N, "La toile rayée goutte au présent, seulement."),
        ),
        "fromage,vrai",
        "store,clair",
        "papier clair",
    )

    # --- FROMAGERIE + MAÎTRESSE ---
    data[("fromagerie", "maitresse", "pain")] = (
        S(
            (N, "La maîtresse a un pain dans le sac, pour après la chanson."),
            (N, "Raphaël le demande. La chanson n'a pas de refrain fini."),
            (N, "Les mots se perdent dans la mélodie, froids."),
            (E, "La chanson d'abord. Le toc. Puis moi, sans chanter."),
            (N, "Le croissant d'eau, à la porte, lâche. Elle se tait."),
            (E, "Bonjour. S'il te plaît, le pain. Merci."),
            (N, "Elle le sort. Il a pris l'odeur du fromage, un peu."),
            (P, "La chanson a eu sa fin. Tes mots, la leur."),
            (M, "Le pain sent la cave. Ta phrase, le calme."),
            (N, "Une miette chantante, presque, reste dans le trou."),
        ),
        S(
            (N, "Sous le store, le pain sent le fromage, drôle, pas grave."),
            (N, "Raphaël le flaire, et rit, sans refaire la chanson."),
            (M, "Tu n'as pas chanté par-dessus. Tu as attendu."),
            (E, "Le toc. Puis les trois mots, parlés, pas chantés."),
            (P, "Parlés, on les a. Le pain aussi, bizarre et bon."),
            (N, "Le croissant d'eau a une courbe de refrain, puis s'arrête."),
            (N, "Une goutte part, une note unique, sur une caisse."),
            (N, "L'écharpe prend l'odeur mixte, four et cave."),
            (N, "La maîtresse reprend le sac, plus léger, plus silencieux."),
            (N, "Papa hausse l'osier. La miette tient, sans mélodie."),
            (N, "Le marché n'est pas une classe. Tant mieux."),
            (N, "Le store écoute, rayure après rayure, sans partition."),
        ),
        "pain,chanson",
        "store,odeur",
        "chanson",
    )
    data[("fromagerie", "maitresse", "pomme")] = (
        S(
            (N, "Une pomme sert de presse-papier, sur une liste, près du marbre."),
            (N, "Raphaël la demande. La maîtresse lit la liste à maman."),
            (N, "La liste est plus longue que sa phrase."),
            (E, "La liste d'abord. Le toc. Puis la pomme, moi."),
            (N, "Le croissant d'eau tombe. La liste s'arrête."),
            (E, "Bonjour. S'il te plaît, la pomme. Merci."),
            (N, "Elle lève le fruit. La liste reste, le point jaune part."),
            (M, "La liste a son papier. La pomme, tes mots."),
            (P, "Plus courte, ta phrase. Entière, pourtant."),
            (N, "Elle se loge dans l'osier, et libère le papier blanc."),
        ),
        S(
            (N, "Sous le store, la pomme n'écrase plus rien. Elle roule, un peu."),
            (N, "Raphaël la cale. Le point jaune vers le croissant d'eau."),
            (M, "Tu as laissé la liste. C'était plus long que toi."),
            (E, "Long. Après le toc, merci a été petit, et vrai."),
            (P, "Petit, vrai, entier. On l'a, avec la pomme."),
            (N, "Une goutte part du croissant, et n'écrase rien, elle non plus."),
            (N, "L'osier sent l'encre, un instant, puis le fruit."),
            (N, "La maîtresse plie la liste. Le marbre redevient un lac."),
            (N, "L'écharpe fait un nid. La pomme cesse de rouler."),
            (N, "Papa ne lit rien. Il a écouté, c'est autre chose."),
            (N, "Le pigeon n'a pas de liste. Il a sa miette."),
            (N, "La toile rayée tient le croissant, sans l'écraser."),
        ),
        "pomme,liste",
        "store,liste",
        "presse-papier",
    )
    data[("fromagerie", "maitresse", "fromage")] = (
        S(
            (N, "Le fromage du goûter est celui que Raphaël veut, presque le même."),
            (N, "Il parle. Elle dit le mot goûter, en même temps."),
            (N, "Deux mots se cognent. Aucun n'arrive."),
            (E, "Goûter d'abord. Le toc. Puis moi, le mien."),
            (N, "Le croissant d'eau, à la porte, lâche. Goûter se tait."),
            (E, "Bonjour. S'il te plaît, ce fromage. Merci."),
            (N, "Elle en prend un second, pour lui, papier à pois."),
            (P, "Deux goûters. Deux tours. Tes mots, au second."),
            (M, "Le papier à pois se tait. On t'a entendu."),
            (N, "Les pois passent dans le trou, un à un, comme des gouttes."),
        ),
        S(
            (N, "Sous le store, le papier à pois imite le croissant d'eau, un peu."),
            (N, "Raphaël compte trois pois, comme trois mots, sans leçon."),
            (M, "Tu as laissé le goûter. Puis tu as demandé le tien."),
            (E, "Après le toc. Merci, sur les pois."),
            (P, "Sur les pois, on l'a. Le fromage aussi."),
            (N, "Le croissant d'eau a des bords irréguliers, comme des pois."),
            (N, "Une goutte part, ronde, et tape le pavé, nette."),
            (N, "L'osier sent le lait, et l'encre des pois, imaginaire."),
            (N, "La maîtresse range le goûter. Le sac ferme, enfin."),
            (N, "Papa cale le fond. Aucun poi ne s'échappe."),
            (N, "Raphaël pose deux doigts sur un poi, comme sur une oreille."),
            (N, "Le store, au-dessus, a fini de couper les phrases."),
        ),
        "fromage,pois",
        "store,pois",
        "pois",
    )

    return data


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
            (N, "Le premier bruit n'est pas une voix."),
            (N, "C'est un toc, sur une chaussure, sous le store."),
            (N, "Le marché du village s'abrite sous une toile rayée."),
            (N, "Raphaël connaît les caisses, le pain, le fromage."),
            (N, "Sur la toile, une forme paraît nouvelle."),
            (N, "Un croissant d'eau, plus sombre que les rayures."),
            (N, "Une goutte y tremble, ronde, prête à partir."),
            (N, "Papa porte le panier d'osier, anse un peu rêche."),
            (N, "Le panier a un trou, petit, près du fond."),
            (N, "Maman noue l'écharpe rouge de Raphaël."),
            (N, "Ça sent le pain chaud, et le bois mouillé."),
            (N, "Un pigeon picore une miette, près d'une caisse."),
            (N, "En ce moment, Raphaël prend l'anse, trop vite."),
            (E, "Les trois mots, tout de suite !"),
            (N, "Papa parle à maman, du fromage, de la liste."),
            (E, "Bonjour s'il te plaît mer !"),
            (N, "Les mots se cognent aux phrases de papa."),
            (N, "La goutte tombe."),
            (N, "Toc, sur la chaussure."),
            (N, "Le dernier mot n'est pas arrivé."),
            (E, "Ils n'ont pas entendu !"),
            (N, "Son sourire disparaît."),
            (N, "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
            (P, "Tu disais quelque chose, Raphaël ?"),
            (E, "Les trois mots se sont cassés."),
            (M, "On t'écoute, quand la goutte a fini."),
            (P, "Merci d'avoir attendu ma phrase."),
            (N, "Le croissant d'eau se reforme, minuscule, sur la toile."),
        ),
        "opening",
        "goutte,marche",
        {"emphasis": "croissant d'eau"},
    )

    put(
        "CHK_T0001_P0000",
        L(
            (N, "Trois coins du marché peuvent recevoir les mots, entiers."),
            (P, "La boulangerie, l'étal, ou la fromagerie ?"),
            (M, "Où veux-tu les porter, jusqu'au bout ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "la boulangerie", "option_2_label": "l'étal", "option_3_label": "la fromagerie"}},
    )

    put(
        "CHK_T0001_P0001",
        L(
            (N, "Raphaël pousse la porte. Une cloche fait ding, trop fort."),
            (N, "L'air chaud sent le beurre, et un peu de farine."),
            (N, "Il lance les trois mots, pile avec le ding."),
            (E, "Bonjour s'il te—"),
            (N, "La cloche recouvre tout. Personne ne se tourne."),
            (N, "Ses joues chauffent. Il veut crier plus fort."),
            (N, "Papa s'accroupit, à la même hauteur, près du panier."),
            (N, "Raphaël refuse de foncer. Il attend que le bronze finisse."),
            (E, "Quand la cloche s'est tue, je dis bonjour ?"),
            (P, "Elle s'est tue. Nous t'écoutons."),
            (E, "Bonjour."),
            (N, "Un croissant d'eau, à la vitre, garde une goutte ronde."),
            (M, "Le premier mot est arrivé. Les autres, plus tard."),
        ),
        "action",
        "cloche,beurre",
        {"emphasis": "cloche"},
    )
    put(
        "CHK_T0001_P0001_Q0001",
        L(
            (N, "La cloche a cassé la phrase, à la porte."),
            (M, "Quel mot Raphaël dit-il, quand elle s'est tue ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "bonjour",
                "accepted_examples": "bonjour | il dit bonjour | bonjour s'il te plaît | merci",
                "retry_prompt": "La cloche s'est tue. Le mot d'accueil ?",
                "engine_ok_text": "Oui, il dit bonjour.",
                "engine_near_text": "Tu es près. Écoute la cloche, puis le mot.",
            },
        },
    )
    put(
        "CHK_T0001_P0001_C0001",
        L(
            (M, "Oui. Il dit bonjour, quand la cloche s'est tue."),
            (N, "Papa se redresse. La farine flotte, un nuage."),
            (P, "Tes mots ont de la place, maintenant."),
            (E, "Le pain est là. Les trois mots, presque."),
            (N, "La cloche reste silencieuse, un moment."),
            (N, "À la vitre, le croissant d'eau ne tombe pas."),
            (M, "Qui va les entendre, la suite ?"),
        ),
        "confirm",
        "cloche",
        {"emphasis": "bonjour"},
    )
    put(
        "CHK_T0001_P0001_T0002_P0000",
        L(
            (N, "Dans la chaleur du four, une oreille doit se choisir."),
            (P, "La boulangère, le voisin, ou la maîtresse ?"),
            (M, "À qui dire les mots, jusqu'au bout ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "la boulangère", "option_2_label": "le voisin", "option_3_label": "la maîtresse"}},
    )

    put(
        "CHK_T0001_P0002",
        L(
            (N, "Raphaël s'arrête sous le store, devant l'étal."),
            (N, "Les caisses sentent le bois mouillé. Des pommes brillent."),
            (N, "Un papier vert claque au vent, pile sur sa voix."),
            (E, "Bonjour, je voudrais—"),
            (N, "Le papier parle plus fort. Le pigeon s'envole."),
            (N, "Les mots s'envolent aussi. Raphaël serre l'anse."),
            (N, "Maman s'accroupit, à sa hauteur, près d'une caisse."),
            (N, "Il refuse de crier. Il attend que le vert se tienne."),
            (E, "Quand le papier ne claque plus, je dis bonjour ?"),
            (M, "Il ne claque plus. Je t'écoute."),
            (E, "Bonjour."),
            (N, "Au-dessus, le croissant d'eau brille, plus sombre."),
            (P, "Le premier mot a posé le pied. La suite ?"),
        ),
        "action",
        "papier,vent",
        {"emphasis": "papier vert"},
    )
    put(
        "CHK_T0001_P0002_Q0001",
        L(
            (N, "Le papier vert a parlé plus fort que Raphaël."),
            (P, "Quel mot dit-il, quand le papier se tait ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "bonjour",
                "accepted_examples": "bonjour | il dit bonjour | bonjour s'il te plaît | merci",
                "retry_prompt": "Le papier se tait. Le mot d'accueil ?",
                "engine_ok_text": "Oui, il dit bonjour.",
                "engine_near_text": "Tu es près. Écoute le papier, puis le mot.",
            },
        },
    )
    put(
        "CHK_T0001_P0002_C0001",
        L(
            (P, "Oui. Il dit bonjour, quand le papier se tait."),
            (N, "Le pigeon se pose plus loin, miette nouvelle."),
            (M, "Tes mots ont un étal, maintenant, sans claquement."),
            (E, "La pomme est là. Les trois mots, presque."),
            (N, "Le papier vert pend, mouillé, sage."),
            (N, "Le croissant d'eau, au-dessus, ne tombe pas."),
            (P, "Qui va entendre la suite, ici ?"),
        ),
        "confirm",
        "papier",
        {"emphasis": "bonjour"},
    )
    put(
        "CHK_T0001_P0002_T0002_P0000",
        L(
            (N, "Sous le store, une oreille doit se choisir, parmi les caisses."),
            (M, "La boulangère, le voisin, ou la maîtresse ?"),
            (P, "À qui porter les mots, entiers ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "la boulangère", "option_2_label": "le voisin", "option_3_label": "la maîtresse"}},
    )

    put(
        "CHK_T0001_P0003",
        L(
            (N, "Raphaël entre dans la fromagerie. L'air est frais."),
            (N, "Le comptoir de marbre est froid, blanc, lisse."),
            (N, "Quelqu'un commande. Raphaël coupe, trop vite."),
            (E, "Bonjour merci je—"),
            (N, "Le vendeur regarde l'autre. Les mots glissent."),
            (N, "Raphaël sent le froid aux doigts, et aux joues."),
            (N, "Papa s'accroupit, à sa hauteur, loin du marbre."),
            (N, "Il refuse de couper. Il attend que la commande finisse."),
            (E, "Quand l'autre a son fromage, je dis bonjour ?"),
            (P, "Il l'a. Le marbre t'écoute. Nous aussi."),
            (E, "Bonjour."),
            (N, "À la porte, le croissant d'eau fait une virgule."),
            (M, "Le premier mot a pris le froid, sans se casser."),
        ),
        "action",
        "marbre,commande",
        {"emphasis": "marbre"},
    )
    put(
        "CHK_T0001_P0003_Q0001",
        L(
            (N, "La commande a recouvert sa phrase, sur le marbre."),
            (M, "Quel mot dit Raphaël, après l'autre client ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "bonjour",
                "accepted_examples": "bonjour | il dit bonjour | bonjour s'il te plaît | merci",
                "retry_prompt": "L'autre a fini. Le mot d'accueil ?",
                "engine_ok_text": "Oui, il dit bonjour.",
                "engine_near_text": "Tu es près. Attends le client, puis le mot.",
            },
        },
    )
    put(
        "CHK_T0001_P0003_C0001",
        L(
            (M, "Oui. Il dit bonjour, après l'autre client."),
            (N, "Un papier blanc attend, plié, près de la balance."),
            (P, "Tes mots ont du frais, et de la place."),
            (E, "Le fromage est là. Les trois mots, presque."),
            (N, "Le marbre reste froid, sans avaler la suite."),
            (N, "Le croissant d'eau, à la porte, tient sa goutte."),
            (M, "Qui va entendre le reste, ici ?"),
        ),
        "confirm",
        "marbre",
        {"emphasis": "bonjour"},
    )
    put(
        "CHK_T0001_P0003_T0002_P0000",
        L(
            (N, "Dans le frais du marbre, une oreille doit se choisir."),
            (P, "La boulangère, le voisin, ou la maîtresse ?"),
            (M, "À qui dire les mots, sans couper ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "la boulangère", "option_2_label": "le voisin", "option_3_label": "la maîtresse"}},
    )

    lieu_key = {"1": "boulangerie", "2": "etal", "3": "fromagerie"}
    pers_key = {"1": "boulangere", "2": "voisin", "3": "maitresse"}
    obj_key = {"1": "pain", "2": "pomme", "3": "fromage"}

    t2 = t2_scenes()
    t3q = {
        ("boulangerie", "boulangere"): "Les pièces se sont tues. Que mettre dans l'osier ?",
        ("boulangerie", "voisin"): "Le pigeon du récit s'est tu. Que demander ?",
        ("boulangerie", "maitresse"): "Le dessin est rangé. Que mettre dans le panier ?",
        ("etal", "boulangere"): "L'aiguille s'est arrêtée. Que mettre dans l'osier ?",
        ("etal", "voisin"): "Le prix est dit. Que demander, maintenant ?",
        ("etal", "maitresse"): "La feuille est choisie. Que mettre sous le store ?",
        ("fromagerie", "boulangere"): "Le lait est dit. Que demander, sur le marbre ?",
        ("fromagerie", "voisin"): "Hier s'est tu. Que mettre dans le trou ?",
        ("fromagerie", "maitresse"): "La chanson est finie. Que demander, à ton tour ?",
    }

    for li in "123":
        for pe in "123":
            lieu, pers = lieu_key[li], pers_key[pe]
            lines, sons, emph = t2[(lieu, pers)]
            cid = f"CHK_T0001_P000{li}_T0002_P000{pe}"
            put(cid, lines, "obstacle", sons, {"emphasis": emph})
            put(
                f"{cid}_T0003_P0000",
                L(
                    (N, t3q[(lieu, pers)]),
                    (M, "Le pain, une pomme, ou un fromage ?"),
                ),
                "choice",
                "",
                {"fields": {"option_1_label": "le pain", "option_2_label": "une pomme", "option_3_label": "un fromage"}},
            )

    scenes = t3_scenes()
    for li in "123":
        for pe in "123":
            for ob in "123":
                lieu, pers, obj = lieu_key[li], pers_key[pe], obj_key[ob]
                passage, ending, s3, se, emph = scenes[(lieu, pers, obj)]
                base = f"CHK_T0001_P000{li}_T0002_P000{pe}_T0003_P000{ob}"
                put(base, passage, "resolution", s3, {"emphasis": emph})
                put(f"{base}_F0001", ending, "ending", se, {"emphasis": "croissant d'eau"})

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
        "Sous le store goutteux du marché, un croissant d'eau plus sombre marque la toile. "
        "Raphaël veut faire arriver trois mots jusqu'au bout, pour remplir le panier d'osier troué. "
        "Sa première phrase se casse contre la liste de papa, et une goutte tape sa chaussure. "
        "La boulangerie, l'étal ou la fromagerie changent le bruit qui recouvre. "
        "La boulangère, le voisin ou la maîtresse changent l'oreille à attendre. "
        "Le pain, la pomme ou le fromage changent la trace dans le trou. "
        "Il refuse de foncer, guette le toc du croissant, puis parle dans le silence."
    )
    merged["title"] = "Le store goutteux et les trois mots"
    merged["characters"] = "Raphaël, papa, maman"
    merged["setting"] = "marché sous le store, boulangerie, étal, fromagerie"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])

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
                "# TREE-COL-035 — Le store goutteux et les trois mots",
                "",
                "- **Public :** N2, 4–5 ans, lecture interactive familiale",
                "- **Leçon :** COL.POL.001 — demander avec attention et respect (implicite)",
                "- **Secondaire :** COL.ECO.002 — attendre son tour de parole (implicite)",
                "- **Personnages :** Raphaël, papa, maman",
                "- **Lieu :** marché sous le store, boulangerie, étal, fromagerie",
                "- **Objet :** panier d'osier troué, anse rêche",
                "- **Indice unique :** croissant d'eau sur la toile rayée, payé au climax",
                "- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes",
                "",
                "Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.",
                "",
                "## Promesse narrative",
                "",
                "Sous le store goutteux, Raphaël veut faire arriver trois mots jusqu'au bout, pour remplir le panier. "
                "Sa première phrase se casse contre la liste de papa ; une goutte tape sa chaussure. "
                "La boulangerie, l'étal ou la fromagerie changent le bruit qui recouvre. "
                "La boulangère, le voisin ou la maîtresse changent l'oreille à attendre. "
                "Le pain, la pomme ou le fromage changent la trace dans le trou. "
                "Il refuse de foncer, guette le toc du croissant d'eau, puis parle dans le silence.",
                "",
                "## Vécu",
                "",
                "Raphaël veut les trois mots **maintenant**. Il coupe. Personne n'entend. Le sourire disparaît. "
                "Envie et inquiétude se bousculent. Papa s'accroupit. Un merci vécu : attendre la phrase. "
                "Tours : envie de couper, retenue, écoute réelle, plaisir d'être entendu. "
                "La leçon se voit : parler dans les mots des autres casse la phrase ; attendre le toc la livre entière. "
                "Pas de « on dit bonjour, on dit s'il te plaît, on dit merci » récité.",
                "",
                "## Améliorations",
                "",
                "- Titre noyau conservé. Ouverture par un toc, pas un gabarit v2.",
                "- Indice unique dès le début (croissant d'eau), payé à chaque climax T3 et au revers.",
                "- Première tentative ratée dès l'ouverture (liste + goutte sur la chaussure).",
                "- T1/T2/T3 changent l'obstacle, pas seulement le décor.",
                "- Revers allongé : 12 phrases, objet + trou + croissant + toc du début.",
                "- Tics « encore / déjà / tout doux / tout calme » retirés.",
                "- Adulte conversationnel (papa/maman). Maîtresse narrée, pas en rôle.",
                "- Un merci vécu, lié au geste (attendre la phrase).",
                "- 27 fins textuellement distinctes.",
                f"- TTS par fonction (opening / choice / clue / confirm / action / obstacle / resolution / ending).",
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


if __name__ == "__main__":
    build()
