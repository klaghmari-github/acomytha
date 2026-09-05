#!/usr/bin/env python3
"""TREE-AUT-003 — La tasse de cacao et la vitre (F-NAR-019, N2, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-AUT-003"
N2 = 15
TITLE = "La tasse de cacao et la vitre"
CHILD = "enfant-f"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|encore|déjà|deja)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="tasse étoilée",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=2; destinataire=enfant; sous_texte=la_goutte_n_attend_pas; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_recherche; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="tasse",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=elle_est_revenue_la_chercher; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="étoile",
        note="arc=confirmation; intention=relancer; emotion=élan_prudent; intensite=1; destinataire=enfant; sous_texte=la_tasse_est_reprise; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=la_premiere_idee_rate; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_deuxieme_imprevu_est_plus_ruse; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="soleil",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_trait_du_debut_devient_un_rayon; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="goutte",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_goutte_a_paye_le_crayon; tempo=posé; sourire=léger; respiration=ample",
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": (
        "reprendre | elle reprend | ses affaires | la tasse | le crayon | "
        "l'écharpe | la tasse étoilée | tasse"
    ),
    "retry_prompt": "Elle revient la reprendre. Mila fait quoi ?",
    "engine_ok_text": "Oui, elle reprend la tasse.",
    "engine_near_text": "Tu es tout près. Écoute l'indice une autre fois.",
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        starts.append(tok)
        out.append(f"{role}|{ph}")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {starts[i]}")
        else:
            run = 1
    return out


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
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
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
    tag = m.get("pitchTag")
    if tag:
        body = f"<{tag}>{body}</{tag}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines)
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m.get("emphasis") or ""
    nc["pause_before_ms"] = extra.get("pause_before_ms", 0)
    nc["pause_after_ms"] = m["pause"]
    nc["pause_sentence_ms"] = m["sentence"]
    nc["style_energy"] = m["energy"]
    nc["style_contour"] = m["contour"]
    nc["noise_scale_piper"] = m["noise"]
    nc["kokoro_speed"] = m["speed"]
    nc["melo_speed"] = m["speed"]
    nc["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    nc["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    nc["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    nc["notes"] = extra.get("notes", m["note"])
    nc["night_policy"] = extra.get("night_policy", "play")
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


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


N, E, P, M = "narrateur", CHILD, "papa", "maman"


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


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, phrase = raw.split("|", 1)
        for sent in split_sents(phrase.strip()):
            out.append(f"{role}|{sent}")
    return out


OPENING = L(
    f"{N}|La pluie vient de quitter le toit.",
    f"{N}|Ça sent le cacao, chaud, dans toute la maison.",
    f"{N}|Au salon, la vitre du campement s'est embuée.",
    f"{N}|Une goutte glisse, lente, et laisse un trait brillant.",
    f"{N}|On dirait un crayon, tout seul.",
    f"{P}|J'ai posé la tasse étoilée.",
    f"{N}|L'anse porte une petite étoile bleue.",
    f"{N}|La tasse fait toc sur la soucoupe, puis fume.",
    f"{M}|Nina arrive pour le goûter.",
    f"{E}|Je veux un soleil sur la vitre !",
    f"{P}|La goutte descend, Mila.",
    f"{N}|En ce moment, Mila tend les deux mains.",
    f"{N}|La vapeur lui pique le nez.",
    f"{E}|Trop chaud ! Je dessine d'abord !",
    f"{M}|Il manque la cuillère-étoile ?",
    f"{P}|Ou la menthe du jardin.",
    f"{N}|Le carré de laine dort dans la chambre.",
    f"{E}|Je cours ! Le soleil n'attend pas.",
)

T1 = {
    1: {
        "sons": "chaise,casserole",
        "emphasis": "cuillère-étoile",
        "passage": L(
            f"{N}|Mila pousse la porte de la cuisine.",
            f"{N}|Ça sent le cacao, plus fort, près de la casserole.",
            f"{N}|Sur la table du cacao, la cuillère-étoile attend.",
            f"{N}|Elle a une perle jaune au bout du manche.",
            f"{E}|Je la prends ! Le soleil, après !",
            f"{N}|Son doigt trace un rond sur la vitre de l'évier.",
            f"{N}|Le rond reste pâle, presque invisible.",
            f"{E}|Ça ne marche pas.",
            f"{N}|Ses épaules baissent. La vapeur cache le verre.",
            f"{M}|Ta tasse étoilée est au salon.",
            f"{P}|Tu la reprends, Mila ?",
            f"{E}|Oui. Mon doigt avait froid.",
            f"{N}|Elle saisit la cuillère. La perle tape, tic.",
            f"{N}|Elle revient vers le campement, moins vite.",
        ),
        "question": L(
            f"{N}|Mila a laissé la tasse au salon.",
            f"{M}|Elle est revenue. Elle a fait quoi ?",
        ),
        "confirm": L(
            f"{N}|Mila pose la cuillère près de la soucoupe.",
            f"{N}|Elle reprend la tasse étoilée à deux mains.",
            f"{N}|L'étoile bleue réapparaît, un peu de vapeur autour.",
            f"{E}|Je t'ai. On va au campement.",
            f"{M}|Merci, je vois l'étoile, maintenant.",
            f"{P}|Tu souffles un peu, avant de boire ?",
            f"{E}|Un petit souffle.",
            f"{N}|Le toc de la soucoupe répond, clair.",
            f"{M}|Tu emportes un jeu, pour le campement ?",
            f"{E}|Oui. Pour attendre Nina.",
        ),
        "t2q": L(
            f"{N}|Un jeu peut aider le campement de la vitre.",
            f"{P}|Le ballon rouge, le seau bleu, ou le doudou ?",
        ),
    },
    2: {
        "sons": "goutte,feuilles",
        "emphasis": "menthe",
        "passage": L(
            f"{N}|Mila ouvre la porte du jardin.",
            f"{N}|Le passage des gouttes brille sur les dalles.",
            f"{N}|Sous la gouttière, la menthe sent fort.",
            f"{E}|Une feuille, pour le cacao de Nina !",
            f"{N}|Elle tire trop vite. La tige plie, rien.",
            f"{E}|Elle reste collée.",
            f"{P}|Regarde le pied, près de la pierre.",
            f"{N}|Mila se baisse. Une feuille se détache, mouillée.",
            f"{N}|Au salon, la tasse fume sans elle.",
            f"{M}|Ta tasse étoilée t'attend.",
            f"{E}|Je l'ai oubliée.",
            f"{N}|Elle rentre, la menthe au creux de la main.",
            f"{P}|Tu la reprends, la tasse ?",
            f"{E}|Oui, papa.",
            f"{N}|Une dalle claque derrière elle, puis se tait.",
        ),
        "question": L(
            f"{N}|Mila a laissé la tasse au salon.",
            f"{P}|Elle est revenue. Elle a fait quoi ?",
        ),
        "confirm": L(
            f"{N}|Mila pose la menthe près de la soucoupe.",
            f"{N}|Elle reprend la tasse étoilée à deux mains.",
            f"{N}|L'étoile bleue réapparaît, un peu de vapeur autour.",
            f"{E}|Je t'ai. La feuille aussi.",
            f"{M}|Merci, je vois l'étoile, maintenant.",
            f"{P}|Tu souffles un peu, avant de boire ?",
            f"{E}|Un petit souffle.",
            f"{N}|Le toc de la soucoupe répond, clair.",
            f"{M}|Tu emportes un jeu, pour le campement ?",
            f"{E}|Oui. Pour attendre Nina.",
        ),
        "t2q": L(
            f"{N}|Un jeu peut aider le campement de la vitre.",
            f"{M}|Le ballon rouge, le seau bleu, ou le doudou ?",
        ),
    },
    3: {
        "sons": "tissu,oreiller",
        "emphasis": "carré de laine",
        "passage": L(
            f"{N}|Mila entre dans la chambre, trop pressée.",
            f"{N}|Le nid de laine est un tas de couvertures.",
            f"{N}|Le carré beige cache son bord sous l'oreiller.",
            f"{E}|Pour tenir la tasse, au chaud.",
            f"{N}|Elle fouille. Un chausson tombe, puis un livre.",
            f"{N}|Pas de carré. Ses mains se ferment, vides.",
            f"{E}|Il a disparu.",
            f"{M}|Sous l'oreiller, peut-être ?",
            f"{N}|Mila soulève l'oreiller. Le carré est là, tiède.",
            f"{P}|Et la tasse étoilée ?",
            f"{E}|Elle est restée au salon.",
            f"{N}|Elle revient, le carré contre la poitrine.",
            f"{M}|Tu la reprends ?",
            f"{E}|Oui. J'ai besoin d'elle.",
        ),
        "question": L(
            f"{N}|Mila a laissé la tasse au salon.",
            f"{M}|Elle est revenue. Elle a fait quoi ?",
        ),
        "confirm": L(
            f"{N}|Mila glisse le carré sous la soucoupe.",
            f"{N}|Elle reprend la tasse étoilée à deux mains.",
            f"{N}|L'étoile bleue réapparaît, un peu de vapeur autour.",
            f"{E}|Je t'ai. Le carré aussi.",
            f"{M}|Merci, je vois l'étoile, maintenant.",
            f"{P}|Tu souffles un peu, avant de boire ?",
            f"{E}|Un petit souffle.",
            f"{N}|Le toc de la soucoupe répond, clair.",
            f"{M}|Tu emportes un jeu, pour le campement ?",
            f"{E}|Oui. Pour attendre Nina.",
        ),
        "t2q": L(
            f"{N}|Un jeu peut aider le campement de la vitre.",
            f"{P}|Le ballon rouge, le seau bleu, ou le doudou ?",
        ),
    },
}


def t2_scenes() -> dict[tuple[int, int], tuple]:
    data: dict[tuple[int, int], tuple] = {}
    data[(1, 1)] = (
        L(
            f"{N}|Le ballon rouge attend sous la table du cacao.",
            f"{N}|Une miette brune brille sur le caoutchouc.",
            f"{E}|Toi aussi, au campement !",
            f"{N}|Mila le fait rouler. Il part trop vite.",
            f"{N}|Il tape la soucoupe. Toc, plus fort que la goutte.",
            f"{E}|Oh ! J'ai perdu le trait !",
            f"{N}|Sur la vitre, la goutte a descendu d'un cran.",
            f"{N}|Le petit soleil pâle a un trou, en haut.",
            f"{P}|Le bruit a caché le glissement ?",
            f"{E}|Oui. Mes yeux étaient sur le ballon.",
            f"{N}|Ses lèvres se pincent. Le trait avance sans elle.",
            f"{M}|Tu le poses où, le rouge ?",
            f"{E}|Contre le tapis. Loin de la soucoupe.",
            f"{N}|Le ballon s'arrête. La miette reste.",
            f"{P}|Et le soleil, maintenant ?",
        ),
        "ballon,tasse",
        "ballon",
    )
    data[(1, 2)] = (
        L(
            f"{N}|Le seau bleu trône près de l'évier.",
            f"{N}|Un fond d'eau claire tremble au fond.",
            f"{E}|Il portera la cuillère-étoile !",
            f"{N}|Mila pose le manche. La perle plonge, ploc.",
            f"{N}|L'eau mouille le bois. La perle s'éteint un peu.",
            f"{E}|Elle est triste, maintenant.",
            f"{N}|La vapeur de la tasse rencontre l'eau froide.",
            f"{N}|Un nuage bas cache le bas de la vitre.",
            f"{P}|Tu vois la goutte, là ?",
            f"{E}|Presque plus. C'est flou.",
            f"{N}|Mila secoue le seau. L'eau saute sur le carrelage.",
            f"{M}|La cuillère peut sécher sur le bord ?",
            f"{E}|Oui. Sans l'eau.",
            f"{N}|Elle pose le manche. Tic, sur le métal.",
            f"{P}|Et le soleil, derrière le nuage ?",
        ),
        "seau,eau",
        "seau",
    )
    data[(1, 3)] = (
        L(
            f"{N}|Le doudou beige attend sur une chaise.",
            f"{N}|Il sent le savon, un peu, et le cacao.",
            f"{E}|Tu tiendras la tasse avec moi !",
            f"{N}|Mila l'enroule autour de l'anse.",
            f"{N}|L'étoile bleue disparaît sous le tissu.",
            f"{E}|Ce n'est plus ma tasse !",
            f"{N}|Ses doigts cherchent, tâtonnent, ratent le toc.",
            f"{N}|Sans l'étoile, elle n'ose plus souffler.",
            f"{P}|Elle est dessous, tu crois ?",
            f"{E}|Je ne sais pas. C'est trop caché.",
            f"{N}|Mila recule d'un pas. Le doudou glisse.",
            f"{M}|Tu découvres l'anse, juste un coin ?",
            f"{E}|Un coin. Pour voir l'étoile.",
            f"{N}|Un triangle bleu reparaît, minuscule.",
            f"{P}|Et le soleil, pendant ce temps ?",
        ),
        "tissu,tasse",
        "doudou",
    )
    data[(2, 1)] = (
        L(
            f"{N}|Le ballon rouge attend près du paillasson.",
            f"{N}|Une dalle mouillée lui fait un miroir.",
            f"{E}|Viens voir le passage des gouttes !",
            f"{N}|Mila le pousse. Il file sur l'eau, trop loin.",
            f"{N}|Il rentre en rebondissant, une vraie goutte dessus.",
            f"{E}|Il a volé une goutte du jardin !",
            f"{N}|La goutte du ballon tombe sur la soucoupe.",
            f"{N}|Le toc se noie. La goutte de la vitre accélère.",
            f"{P}|Deux gouttes, et tes yeux où ?",
            f"{E}|Partout. Je n'ai plus le trait.",
            f"{N}|Mila essuie le ballon au paillasson.",
            f"{M}|Tu le poses au sec, contre le mur ?",
            f"{E}|Au sec. Loin de la tasse.",
            f"{N}|Une trace ronde reste sur le bois.",
            f"{P}|Et le soleil, sur le verre ?",
        ),
        "ballon,goutte",
        "ballon",
    )
    data[(2, 2)] = (
        L(
            f"{N}|Le seau bleu attend sous la gouttière.",
            f"{N}|La pluie y a laissé trois gouttes, claires.",
            f"{E}|La menthe voyagera là-dedans !",
            f"{N}|Mila pose la feuille. L'eau l'étale, trop.",
            f"{N}|L'odeur forte s'en va, diluée.",
            f"{E}|Elle ne sent plus rien.",
            f"{N}|Mila rentre le seau. L'eau cloche, molle.",
            f"{N}|Près de la tasse, le cacao sent seul.",
            f"{P}|Ta feuille est trop mouillée ?",
            f"{E}|Oui. Le cacao ne la verra pas.",
            f"{N}|Elle sort la menthe. Une goutte tombe, plic.",
            f"{M}|Sur le bord du seau, pour sécher ?",
            f"{E}|Sur le bord. Sans l'eau.",
            f"{N}|La feuille se redresse, un peu froissée.",
            f"{P}|Et le soleil, pendant que ça sèche ?",
        ),
        "seau,goutte",
        "seau",
    )
    data[(2, 3)] = (
        L(
            f"{N}|Le doudou beige attend sur le banc du jardin.",
            f"{N}|Une feuille collée lui fait une médaille.",
            f"{E}|Tu viens, on sent la menthe ensemble !",
            f"{N}|Mila frotte le doudou contre la feuille.",
            f"{N}|Le tissu prend une tache verte, minuscule.",
            f"{E}|Je l'ai sali.",
            f"{N}|Elle lâche la tasse pour frotter le doudou.",
            f"{N}|Le toc de la soucoupe se fait tout seul, loin.",
            f"{P}|La tasse, Mila ?",
            f"{E}|Elle est restée.",
            f"{N}|Mila s'arrête. Elle n'a pas fini la phrase.",
            f"{M}|Tu la reprends, et le doudou à part ?",
            f"{E}|Oui. Le vert séchera tout seul.",
            f"{N}|Elle reprend l'anse. L'étoile est là.",
            f"{P}|Et le soleil, sur la vitre ?",
        ),
        "tissu,feuilles",
        "doudou",
    )
    data[(3, 1)] = (
        L(
            f"{N}|Le ballon rouge attend sous le lit.",
            f"{N}|Un fil de laine s'est collé dessus.",
            f"{E}|Sors ! On va au campement !",
            f"{N}|Mila tire. Le ballon rebondit contre l'oreiller.",
            f"{N}|Le carré de laine saute, et recouvre l'étoile.",
            f"{E}|Je ne vois plus ma tasse !",
            f"{N}|Sous le beige, le toc est sourd, étouffé.",
            f"{N}|La goutte de la vitre du lit a disparu.",
            f"{P}|Le carré a mangé l'anse ?",
            f"{E}|Oui. Et le bruit aussi.",
            f"{N}|Mila soulève la laine. L'étoile cligne.",
            f"{M}|Le ballon, sous la chaise, cette fois ?",
            f"{E}|Sous la chaise. Sans le fil.",
            f"{N}|Elle ôte le fil. Il reste dans sa poche.",
            f"{P}|Et le soleil du salon ?",
        ),
        "ballon,tissu",
        "ballon",
    )
    data[(3, 2)] = (
        L(
            f"{N}|Le seau bleu attend près de la commode.",
            f"{N}|Un chausson y dort, tout seul.",
            f"{E}|Le carré voyagera là-dedans !",
            f"{N}|Mila pose la laine. Le chausson bascule, flop.",
            f"{N}|Le seau penche. Le carré glisse contre le bois.",
            f"{E}|Il va tomber !",
            f"{N}|Elle lâche l'anse pour rattraper le seau.",
            f"{N}|La tasse étoilée reste sur la commode, trop loin.",
            f"{P}|Tu as les mains pleines, là.",
            f"{E}|Trop de choses. J'ai perdu l'étoile.",
            f"{N}|Mila pose le seau. Le chausson rentre sous le lit.",
            f"{M}|Le carré sur tes genoux, la tasse après ?",
            f"{E}|Oui. Un par un.",
            f"{N}|Elle reprend l'anse. Le toc est net, cette fois.",
            f"{P}|Et le soleil du salon ?",
        ),
        "seau,tissu",
        "seau",
    )
    data[(3, 3)] = (
        L(
            f"{N}|Le doudou beige attend dans le nid de laine.",
            f"{N}|À côté, le carré a la même couleur, presque.",
            f"{E}|Je prends le plus doux, pour la tasse !",
            f"{N}|Mila emporte le doudou. Le carré reste.",
            f"{N}|Sur l'anse, le doudou glisse, trop grand.",
            f"{E}|Ce n'est pas le bon.",
            f"{N}|Ses épaules tombent. Deux beiges, et elle s'est trompée.",
            f"{N}|La tasse penche. Un filet de vapeur fuit.",
            f"{P}|Lequel tenait chaud, sous l'oreiller ?",
            f"{E}|Le carré. Pas lui.",
            f"{N}|Mila pose le doudou. Elle reprend le carré.",
            f"{M}|Les deux peuvent venir, chacun sa place ?",
            f"{E}|Le carré sous l'anse. Le doudou à côté.",
            f"{N}|L'étoile bleue reparaît, bien ronde.",
            f"{P}|Et le soleil du salon ?",
        ),
        "tissu,oreiller",
        "doudou",
    )
    return data


T3Q = {
    (1, 1): "Le ballon a volé le bruit de la goutte. Ensuite ?",
    (1, 2): "L'eau du seau a caché le bas du verre. Ensuite ?",
    (1, 3): "Le doudou a caché l'étoile. Ensuite ?",
    (2, 1): "Le ballon a apporté une goutte du jardin. Ensuite ?",
    (2, 2): "L'eau du seau a lavé l'odeur. Ensuite ?",
    (2, 3): "Le doudou a pris une tache verte. Ensuite ?",
    (3, 1): "Le ballon a recouvert l'anse. Ensuite ?",
    (3, 2): "Le seau a trop rempli tes mains. Ensuite ?",
    (3, 3): "Deux beiges, et le mauvais d'abord. Ensuite ?",
}


def t3_end() -> dict[tuple[int, int, int], tuple]:
    """(passage, ending, sons_t3, sons_end, emphasis)."""
    d: dict[tuple[int, int, int], tuple] = {}

    def add(a, b, c, passage, ending, s3, se, emp):
        d[(a, b, c)] = (passage, ending, s3, se, emp)

    # --- cuisine + ballon ---
    add(1, 1, 1, L(
        f"{N}|Le crayon attend dans le pot de bois, un peu froid.",
        f"{E}|Je suis le trait brillant, comme au début.",
        f"{N}|Mila pose le crayon sur la goutte, sans appuyer fort.",
        f"{N}|Le trait devient un rayon, puis un deuxième.",
        f"{P}|Tu copies la goutte, c'est ça ?",
        f"{E}|Oui. Elle était le crayon, avant moi.",
        f"{N}|Le trou du soleil se ferme. Un rond net tient.",
        f"{N}|Le ballon, contre le tapis, garde sa miette.",
        f"{M}|L'étoile de la tasse regarde le dessin ?",
        f"{E}|Elle le chauffe, pour de faux.",
        f"{N}|Mila souffle. La buée recule d'un doigt, puis s'arrête.",
        f"{N}|Le soleil reste. La goutte est un rayon, en bas.",
        f"{P}|Nina va le voir, tu crois ?",
        f"{E}|Oui. Il est prêt.",
    ), L(
        f"{N}|Au campement, le soleil de buée tient, rond.",
        f"{N}|Le ballon s'endort contre le mur, miette au chaud.",
        f"{N}|Le crayon rejoint le pot, une pointe un peu humide.",
        f"{M}|Tu as vu le rayon, en bas ?",
        f"{E}|La goutte s'est arrêtée en rayon.",
        f"{P}|La cuillère-étoile a séché, à côté.",
        f"{N}|L'anse bleue fait un dernier toc, tout petit.",
        f"{N}|Dehors, le toit ne goutte plus.",
        f"{E}|J'ai fait le soleil toute seule.",
        f"{N}|Sur le verre, le trait brillant ne glisse plus.",
    ), "crayon,vitre", "cacao,pluie-legere", "crayon")

    add(1, 1, 2, L(
        f"{N}|La tasse n'est plus trop chaude, juste tiède.",
        f"{E}|Je bois un peu. Mon doigt aura chaud.",
        f"{N}|Mila avale. Ça sent le chocolat, tout près.",
        f"{N}|Son doigt, tiède, reprend le rond pâle.",
        f"{P}|Tu traces avec la chaleur, là ?",
        f"{E}|Oui. Le ballon a volé le bruit. Pas le soleil.",
        f"{N}|Le trou se ferme sous la pulpe, sans crayon.",
        f"{N}|L'étoile bleue tape l'anse, tic, contre sa joue.",
        f"{M}|Elle te parle, l'étoile ?",
        f"{E}|Elle me dit toc.",
        f"{N}|Le ballon reste loin, sage, la miette au centre.",
        f"{N}|La goutte arrive en bas, et devient un sourire.",
        f"{P}|Nina va goûter, tu crois ?",
        f"{E}|Un tout petit fond. Le reste est pour elle.",
    ), L(
        f"{N}|Au campement, la tasse étoilée a un fond brun.",
        f"{N}|Le ballon s'endort, miette tournée vers la vitre.",
        f"{N}|Le soleil de doigt tient, un peu flou, heureux.",
        f"{M}|Ton doigt est tiède, maintenant ?",
        f"{E}|Il a tenu le rond, tout seul.",
        f"{P}|La perle jaune de la cuillère brille au sec.",
        f"{N}|Un dernier toc, plus grave, sur la soucoupe.",
        f"{N}|Le tapis tiède garde la forme de ses genoux.",
        f"{E}|J'ai bu, et le soleil est resté.",
        f"{N}|Sur le verre, le sourire de goutte ne bouge plus.",
    ), "tasse,cacao", "cacao,ballon", "tasse")

    add(1, 1, 3, L(
        f"{N}|L'écharpe a glissé d'une épaule, laine grise.",
        f"{E}|Je me couvre. Puis je souffle sur le verre.",
        f"{N}|Mila noue l'écharpe. Un nuage neuf naît sous sa bouche.",
        f"{N}|Le trou du soleil se remplit de buée, toute neuve.",
        f"{P}|Tu lui redonnes du brouillard, c'est ça ?",
        f"{E}|Oui. Le ballon a fait trop de bruit.",
        f"{N}|Son doigt, au chaud, trace un rond, puis des rayons.",
        f"{N}|L'étoile bleue se cache un instant sous la laine.",
        f"{M}|Tu la laisses respirer, l'anse ?",
        f"{E}|Un coin. Pour le toc.",
        f"{N}|Le ballon, au pied, sert de coussin au campement.",
        f"{N}|La goutte finit dans un rayon, sans se presser.",
        f"{P}|Nina va toucher l'écharpe, tu crois ?",
        f"{E}|Si elle a froid, oui.",
    ), L(
        f"{N}|Au campement, l'écharpe sent le cacao, un peu.",
        f"{N}|Le ballon veille au pied, rouge sur le tapis tiède.",
        f"{N}|Le soleil de souffle touche presque le cadre.",
        f"{M}|Le nuage est revenu, c'est ça ?",
        f"{E}|Il est revenu, juste pour moi.",
        f"{P}|La cuillère-étoile brille au bord.",
        f"{N}|Un toc étouffé sous la laine, puis le silence.",
        f"{E}|J'ai réchauffé la vitre, toute seule.",
        f"{N}|Sur le verre, le rayon-goutte reste, mince et clair.",
    ), "tissu,souffle", "cacao,tissu", "écharpe")

    # --- cuisine + seau ---
    add(1, 2, 1, L(
        f"{N}|Le crayon attend, sec, loin de l'eau du seau.",
        f"{E}|Je dessine au-dessus du nuage, plus haut.",
        f"{N}|Mila lève le crayon. Le rond naît au-dessus du flou.",
        f"{N}|Des rayons descendent, et rencontrent la goutte.",
        f"{P}|Tu travailles au-dessus de l'eau, c'est ça ?",
        f"{E}|Oui. Le seau a volé le bas. Pas le haut.",
        f"{N}|La cuillère-étoile sèche sur le bord, perle terne.",
        f"{N}|Puis la perle reprend un peu de jaune.",
        f"{M}|Elle se réveille, la perle ?",
        f"{E}|Elle sèche. Comme le soleil.",
        f"{N}|Le seau, vide, sert de tabouret au crayon.",
        f"{N}|La goutte accroche un rayon, et s'arrête.",
        f"{P}|Nina verra le haut du soleil, d'abord ?",
        f"{E}|Le haut. Le bas, si le nuage part.",
    ), L(
        f"{N}|Au campement, le soleil habite le haut de la vitre.",
        f"{N}|Le seau bleu, vide, garde une perle d'eau oubliée.",
        f"{N}|Le crayon repose en travers, comme un pont.",
        f"{M}|Tu as dessiné au-dessus du flou ?",
        f"{E}|Le haut du soleil m'a suffi.",
        f"{P}|La cuillère-étoile a retrouvé son tic.",
        f"{N}|Un toc clair, puis le seau qui ne cloche plus.",
        f"{E}|J'ai sauvé le haut du soleil.",
        f"{N}|Sur le verre, le rayon du haut tient la goutte.",
        f"{N}|Le carrelage a une petite flaque, ronde, sage.",
    ), "crayon,seau", "cacao,eau", "crayon")

    add(1, 2, 2, L(
        f"{N}|La tasse est assez tiède pour voyager.",
        f"{E}|Le seau sera le plateau. Sans l'eau.",
        f"{N}|Mila pose la soucoupe dans le seau vide.",
        f"{N}|La tasse étoilée fait un toc plus grave, creux.",
        f"{P}|Elle est à l'abri, maintenant ?",
        f"{E}|Oui. Mes mains tiennent le seau, pas le chaud.",
        f"{N}|Elle avance jusqu'à la vitre. Le nuage s'écarte.",
        f"{N}|Son doigt tiède ferme le rond, tout bas.",
        f"{M}|Le plateau t'a laissé un doigt libre ?",
        f"{E}|Un doigt. Pour le soleil.",
        f"{N}|La cuillère-étoile rentre dans le seau, au sec.",
        f"{N}|La goutte arrive, et pose un point sous le rond.",
        f"{P}|Nina portera le seau, tu crois ?",
        f"{E}|On portera ensemble. C'est lourd un peu.",
    ), L(
        f"{N}|Au campement, le seau bleu est un plateau d'étoile.",
        f"{N}|La tasse y fait toc, plus grave qu'au début.",
        f"{N}|Le soleil de doigt a un point, en bas, comme un pied.",
        f"{M}|Le seau a porté, vraiment ?",
        f"{E}|Il a porté à ma place.",
        f"{P}|La perle jaune est sèche, collée au bord.",
        f"{N}|Un toc creux, puis plus rien que le cacao.",
        f"{E}|J'ai bougé la tasse sans la lâcher.",
        f"{N}|Sur le verre, le point-goutte sert de pied au soleil.",
        f"{N}|Le plateau bleu reste, rond, sous l'anse.",
    ), "tasse,seau", "cacao,seau", "tasse")

    add(1, 2, 3, L(
        f"{N}|L'écharpe attend, sèche, loin de la flaque.",
        f"{E}|Je sèche le manche, puis je souffle.",
        f"{N}|Mila frotte la cuillère-étoile dans la laine.",
        f"{N}|La perle redevient jaune, nette, sans eau.",
        f"{P}|Elle a soif, la laine, ou le bois ?",
        f"{E}|Le bois. La laine boit pour lui.",
        f"{N}|Puis elle souffle. Un nuage neuf chasse le flou.",
        f"{N}|Son doigt trace le rond, plus bas, plus sûr.",
        f"{M}|L'écharpe a deux métiers, là ?",
        f"{E}|Sécher, et me tenir chaud.",
        f"{N}|Le seau vide écoute, collé au mur.",
        f"{N}|La goutte se pose dans un rayon, sans bruit.",
        f"{P}|Nina aura une écharpe, s'il fait froid ?",
        f"{E}|La mienne, un tour, si elle veut.",
    ), L(
        f"{N}|Au campement, l'écharpe a un coin un peu humide.",
        f"{N}|Le seau bleu, vide, garde l'odeur du bois mouillé.",
        f"{N}|Le soleil de souffle est bas, large, posé.",
        f"{M}|La perle a repris son jaune ?",
        f"{E}|Elle brille, toute sèche.",
        f"{P}|La cuillère-étoile fait tic, toute sèche.",
        f"{N}|Un toc, puis le froissement de la laine.",
        f"{E}|J'ai séché, puis j'ai dessiné.",
        f"{N}|Sur le verre, le rayon-goutte est large, presque chaud.",
        f"{N}|Le coin d'écharpe sèche près de l'étoile bleue.",
    ), "tissu,seau", "cacao,tissu", "écharpe")

    # --- cuisine + doudou ---
    add(1, 3, 1, L(
        f"{N}|Le crayon attend. L'étoile n'est plus cachée.",
        f"{E}|Je copie l'étoile sur la vitre.",
        f"{N}|Mila trace cinq branches, lentes, dans la buée.",
        f"{N}|Le soleil a une étoile au milieu, bleue pour de faux.",
        f"{P}|C'est l'anse, ça, au centre ?",
        f"{E}|Oui. Pour qu'on la retrouve, toujours.",
        f"{N}|Le doudou, à côté, garde un pli en triangle.",
        f"{N}|Le pli a la forme de l'anse, un moment.",
        f"{M}|Il a appris l'étoile, le doudou ?",
        f"{E}|Il l'a cachée. Maintenant il la connaît.",
        f"{N}|La goutte glisse dans une branche, et s'arrête.",
        f"{N}|Le toc de la tasse répond, comme un oui.",
        f"{P}|Nina cherchera l'étoile au centre ?",
        f"{E}|Au centre. C'est le secret.",
    ), L(
        f"{N}|Au campement, le soleil a une étoile au ventre.",
        f"{N}|Le doudou garde son pli en triangle, sage.",
        f"{N}|Le crayon a une pointe un peu de buée.",
        f"{M}|L'étoile est allée sur le verre ?",
        f"{E}|Elle est au centre, pour qu'on la trouve.",
        f"{P}|La cuillère-étoile veille, perle vers le dessin.",
        f"{N}|Un toc, puis plus rien que le tapis tiède.",
        f"{E}|J'ai montré l'anse, sans la cacher.",
        f"{N}|Sur le verre, cinq branches tiennent la goutte.",
        f"{N}|Le triangle de tissu regarde l'étoile vraie.",
    ), "crayon,tissu", "cacao,tissu", "crayon")

    add(1, 3, 2, L(
        f"{N}|La tasse est tiède. Le doudou devient soucoupe.",
        f"{E}|Toi dessous. Moi je bois, puis je trace.",
        f"{N}|Mila pose la tasse sur le ventre du doudou.",
        f"{N}|Le toc est mou, drôle, presque un rire.",
        f"{P}|Elle ne glisse plus, comme ça ?",
        f"{E}|Elle est dans un nid. L'étoile se voit.",
        f"{N}|Elle boit. Son doigt tiède ferme le rond.",
        f"{N}|Le doudou sent le cacao, pour de vrai, maintenant.",
        f"{M}|Il a le droit d'avoir l'odeur ?",
        f"{E}|Oui. C'est son métier, ce soir.",
        f"{N}|La goutte pose un point, juste sous l'étoile dessinée.",
        f"{N}|Le filet de vapeur est petit, sage.",
        f"{P}|Nina s'assoira sur le doudou, tu crois ?",
        f"{E}|À côté. Le nid, c'est pour la tasse.",
    ), L(
        f"{N}|Au campement, le doudou est une soucoupe molle.",
        f"{N}|La tasse étoilée y fait un toc mou, content.",
        f"{N}|Le soleil de doigt a un point, sous une étoile.",
        f"{M}|Le toc est devenu un rire ?",
        f"{E}|Un toc mou, comme un rire.",
        f"{P}|La cuillère-étoile dort sur le tissu, en travers.",
        f"{N}|Un toc mou, puis l'odeur du savon et du cacao.",
        f"{E}|J'ai bu sans cacher l'anse.",
        f"{N}|Sur le verre, le point-goutte salue l'étoile du milieu.",
        f"{N}|Le nid beige garde un rond un peu plus foncé.",
    ), "tasse,tissu", "cacao,tissu", "tasse")

    add(1, 3, 3, L(
        f"{N}|L'écharpe et le doudou se touchent, deux beiges.",
        f"{E}|L'écharpe pour moi. Le doudou pour l'anse, un coin.",
        f"{N}|Mila se couvre. Elle laisse l'étoile hors du tissu.",
        f"{N}|Puis elle souffle. Un nuage neuf, tout proche.",
        f"{P}|Deux tissus, et l'étoile dehors, c'est ça ?",
        f"{E}|Dehors. Pour le toc, et pour Nina.",
        f"{N}|Son doigt trace un rond large, chaud de l'écharpe.",
        f"{N}|Le doudou tient l'anse, sans l'avaler.",
        f"{M}|Ils se partagent le travail ?",
        f"{E}|Oui. Moi le souffle. Eux le chaud.",
        f"{N}|La goutte finit en rayon, contre l'épaule de laine.",
        f"{N}|Un toc net, enfin, sous le coin de doudou.",
        f"{P}|Nina aura le doudou, ou l'écharpe ?",
        f"{E}|Le doudou, si elle a froid aux mains.",
    ), L(
        f"{N}|Au campement, deux tissus gardent la tasse étoilée.",
        f"{N}|L'étoile bleue reste dehors, ronde, visible.",
        f"{N}|Le soleil de souffle est large, presque un manteau.",
        f"{M}|L'anse a eu le droit d'être vue ?",
        f"{E}|Dehors, pour le toc, et pour Nina.",
        f"{P}|La cuillère-étoile dépasse, perle vers la vitre.",
        f"{N}|Un toc net, puis le silence des deux laines.",
        f"{E}|J'ai soufflé, sans cacher l'étoile.",
        f"{N}|Sur le verre, le rayon-goutte touche un pli d'écharpe.",
        f"{N}|Le coin de doudou garde la forme de l'anse.",
    ), "tissu,souffle", "cacao,tissu", "écharpe")

    # --- jardin + ballon ---
    add(2, 1, 1, L(
        f"{N}|Le crayon attend. Dehors, une goutte du passage brille.",
        f"{E}|Je relie la goutte du dedans à celle du dehors.",
        f"{N}|Mila trace un trait. Les deux gouttes se saluent.",
        f"{N}|Le soleil a un pont, mince, à travers le verre.",
        f"{P}|Le ballon a volé une goutte, et toi tu la rends ?",
        f"{E}|Je la rends au dessin. Pas au ballon.",
        f"{N}|La menthe, au sec, pose une odeur verte sur le trait.",
        f"{N}|Le ballon, au mur, a une trace ronde, sèche.",
        f"{M}|Le jardin est dans le salon, là ?",
        f"{E}|Un tout petit jardin, sur la vitre.",
        f"{N}|La goutte du dedans s'arrête au milieu du pont.",
        f"{N}|Le toc de la tasse dit oui, tout bas.",
        f"{P}|Nina verra le pont, d'abord ?",
        f"{E}|Le pont. Puis le cacao à la menthe.",
    ), L(
        f"{N}|Au campement, deux gouttes se tiennent par un trait.",
        f"{N}|Le ballon, sec, garde un rond plus pâle au flanc.",
        f"{N}|Le crayon sent la menthe, un peu, à la pointe.",
        f"{M}|Le dedans a parlé au dehors ?",
        f"{E}|Les deux gouttes se tiennent.",
        f"{P}|La feuille de menthe a séché, en virgule.",
        f"{N}|Un toc, puis une dalle qui ne claque plus.",
        f"{E}|J'ai rendu la goutte au soleil.",
        f"{N}|Sur le verre, le pont mince ne glisse plus.",
        f"{N}|Le passage des gouttes, dehors, s'est tu.",
    ), "crayon,goutte", "cacao,feuilles", "crayon")

    add(2, 1, 2, L(
        f"{N}|La tasse est tiède. La menthe attend, moins mouillée.",
        f"{E}|Une feuille dans le cacao. Puis je bois.",
        f"{N}|Mila glisse la menthe. L'odeur verte monte, nette.",
        f"{N}|Elle boit. Son doigt tiède ferme le rond.",
        f"{P}|Le ballon a apporté de l'eau. Toi, la feuille ?",
        f"{E}|La feuille. L'eau, je n'en voulais pas.",
        f"{N}|Le ballon, au sec, ne brille plus.",
        f"{N}|Sur la vitre, un souffle de jardin reste, minuscule.",
        f"{M}|Nina reconnaîtra la menthe ?",
        f"{E}|Avec le nez, avant les yeux.",
        f"{N}|La goutte du dedans pose un point, frais, en bas.",
        f"{N}|Le toc a un goût, presque, dans l'air.",
        f"{P}|Il reste un fond, pour elle ?",
        f"{E}|Un fond vert. Le soleil est à moi.",
    ), L(
        f"{N}|Au campement, le cacao sent la menthe, enfin.",
        f"{N}|Le ballon, sec, tourne sa trace vers la porte.",
        f"{N}|Le soleil de doigt a un point frais, comme une dalle.",
        f"{M}|Le nez a trouvé le jardin ?",
        f"{E}|La menthe, avant les yeux.",
        f"{P}|La feuille flotte, petite barque, dans le fond.",
        f"{N}|Un toc, puis l'odeur verte qui ne part plus.",
        f"{E}|J'ai bu le dehors, sans ouvrir.",
        f"{N}|Sur le verre, le point-goutte est plus clair que les autres.",
        f"{N}|Le paillasson garde un rond de ballon, presque sec.",
    ), "tasse,feuilles", "cacao,menthe", "tasse")

    add(2, 1, 3, L(
        f"{N}|L'écharpe sent l'air du jardin, un peu froid.",
        f"{E}|Je me couvre. La feuille sera un tampon.",
        f"{N}|Mila souffle. Puis elle pose la menthe sur la buée.",
        f"{N}|Une empreinte dentée reste, comme un petit peigne.",
        f"{P}|C'est la feuille, ça, au milieu ?",
        f"{E}|Oui. Le ballon a volé une goutte. Moi, une forme.",
        f"{N}|Des rayons partent de l'empreinte, vers le trait brillant.",
        f"{N}|Le ballon, au mur, n'a plus sa goutte.",
        f"{M}|Le jardin a signé, là ?",
        f"{E}|Il a signé. Pour Nina.",
        f"{N}|La goutte du dedans se loge dans une dent de menthe.",
        f"{N}|L'écharpe tient les épaules, loin de la dalle mouillée.",
        f"{P}|Nina touchera l'empreinte ?",
        f"{E}|Avec les yeux. Les doigts, c'est pour le cacao.",
    ), L(
        f"{N}|Au campement, le soleil a une menthe au cœur.",
        f"{N}|L'écharpe sent l'air du passage des gouttes.",
        f"{N}|Le ballon, sec, n'a plus de miroir au flanc.",
        f"{M}|La feuille a laissé son peigne ?",
        f"{E}|Un tampon de menthe, au milieu.",
        f"{P}|La vraie menthe sèche, à côté, un peu froissée.",
        f"{N}|Un toc, puis un froissement d'écharpe.",
        f"{E}|J'ai tamponné le dehors sur le dedans.",
        f"{N}|Sur le verre, une dent de menthe tient la goutte.",
        f"{N}|Le paillasson ne brille plus.",
    ), "tissu,feuilles", "cacao,tissu", "écharpe")

    # --- jardin + seau ---
    add(2, 2, 1, L(
        f"{N}|Le crayon attend. La menthe sèche sur le bord du seau.",
        f"{E}|Je dessine le chemin de l'eau, du seau à la goutte.",
        f"{N}|Mila trace une rivière mince, de bas en haut.",
        f"{N}|Elle rencontre le trait brillant, et le soleil naît là.",
        f"{P}|Tu racontes le seau, sur la vitre ?",
        f"{E}|Oui. Il a lavé l'odeur. Moi je la dessine.",
        f"{N}|La feuille, froissée, reprend un peu de vert.",
        f"{N}|Le seau, presque vide, a une perle d'eau, unique.",
        f"{M}|Cette perle, c'est le jardin ?",
        f"{E}|La dernière. Le reste est un dessin.",
        f"{N}|La goutte du dedans descend la rivière, et s'arrête.",
        f"{N}|Le toc de la tasse est sec, enfin.",
        f"{P}|Nina suivra la rivière, tu crois ?",
        f"{E}|Du seau jusqu'au soleil.",
    ), L(
        f"{N}|Au campement, une rivière de buée monte vers un soleil.",
        f"{N}|Le seau bleu garde une perle, rien qu'une.",
        f"{N}|Le crayon a le bois un peu taché de vert.",
        f"{M}|L'eau est devenue un chemin ?",
        f"{E}|Une rivière, du seau au soleil.",
        f"{P}|La menthe, sur le bord, a la forme d'un bateau.",
        f"{N}|Un toc sec, puis plus de cloche dans le seau.",
        f"{E}|J'ai dessiné ce que l'eau avait emporté.",
        f"{N}|Sur le verre, la rivière tient la goutte au milieu.",
        f"{N}|Le passage des gouttes, dehors, est terne, fini.",
    ), "crayon,seau", "cacao,eau", "crayon")

    add(2, 2, 2, L(
        f"{N}|La tasse est tiède. La menthe a séché, un peu.",
        f"{E}|Je mets la feuille, puis je bois.",
        f"{N}|Mila pose la menthe. L'odeur revient, moins forte, vraie.",
        f"{N}|Elle boit. Le seau, vide, sert de table basse.",
        f"{P}|Le seau a lavé. Le cacao a rattrapé ?",
        f"{E}|Un peu. Assez pour Nina.",
        f"{N}|Son doigt tiède pose un rond, puis un point d'eau.",
        f"{N}|Le point copie la perle restée dans le seau.",
        f"{M}|Deux perles, une dans le seau, une sur le verre ?",
        f"{E}|Elles se regardent.",
        f"{N}|La goutte du dedans rejoint le point, et s'y couche.",
        f"{N}|Le toc pose la tasse sur le seau, grave et calme.",
        f"{P}|Il reste un fond, au goût de jardin ?",
        f"{E}|Un fond. Le soleil est à nous deux.",
    ), L(
        f"{N}|Au campement, le seau bleu est une table de tasse.",
        f"{N}|Le cacao sent une menthe discrète, revenue.",
        f"{N}|Le soleil de doigt a une perle, jumelle du seau.",
        f"{M}|Les deux perles se sont vues ?",
        f"{E}|Une dans le seau, une sur le verre.",
        f"{P}|La feuille a coulé, puis elle flotte, petite.",
        f"{N}|Un toc grave, creux, comme un puits gentil.",
        f"{E}|J'ai rendu l'odeur, sans l'eau de trop.",
        f"{N}|Sur le verre, la perle-goutte ne glisse plus.",
        f"{N}|Le seau, table, ne cloche plus.",
    ), "tasse,seau", "cacao,menthe", "tasse")

    add(2, 2, 3, L(
        f"{N}|L'écharpe attend dans l'entrebâillement de la porte.",
        f"{E}|Je me couvre. L'air du jardin peut rester dehors.",
        f"{N}|Mila noue. Puis elle souffle un nuage, net, au chaud.",
        f"{N}|La menthe, au bord du seau, pose son ombre sur le verre.",
        f"{P}|Tu dessines l'ombre, ou le soleil ?",
        f"{E}|Les deux. L'ombre est une feuille. Le soleil, autour.",
        f"{N}|Des rayons évitent l'ombre, puis la saluent.",
        f"{N}|Le seau, vide, cale la porte, un peu.",
        f"{M}|Il garde le jardin à sa place ?",
        f"{E}|Oui. L'écharpe aussi, sur moi.",
        f"{N}|La goutte se loge dans l'ombre de menthe, et s'arrête.",
        f"{N}|Un toc, puis le claquement mou du seau contre le bois.",
        f"{P}|Nina passera la porte, tu crois ?",
        f"{E}|Le seau laissera un passage, juste assez.",
    ), L(
        f"{N}|Au campement, un soleil entoure une ombre de menthe.",
        f"{N}|L'écharpe sent l'air froid, arrêté à la porte.",
        f"{N}|Le seau bleu cale le bois, vide et utile.",
        f"{M}|L'ombre est devenue un cœur ?",
        f"{E}|L'ombre de la feuille, au centre.",
        f"{P}|La vraie menthe sèche, collée au bord, en virgule.",
        f"{N}|Un toc, puis plus d'air froid sur les chevilles.",
        f"{E}|J'ai tenu le jardin à sa place.",
        f"{N}|Sur le verre, l'ombre-goutte est verte pour de faux.",
        f"{N}|La porte ne claque plus.",
    ), "tissu,seau", "cacao,tissu", "écharpe")

    # --- jardin + doudou ---
    add(2, 3, 1, L(
        f"{N}|Le crayon attend. La tache verte du doudou a pâli.",
        f"{E}|Je dessine un nuage en forme de menthe, autour du soleil.",
        f"{N}|Mila trace un ovale denté, puis le rond au milieu.",
        f"{N}|Le doudou, à côté, montre sa médaille presque sèche.",
        f"{P}|Tu copies la tache, c'est ça ?",
        f"{E}|Je la change. Elle devient un nuage, pas une saleté.",
        f"{N}|La goutte glisse dans l'ovale, et s'y cache, contente.",
        f"{N}|Le toc de la tasse est net. L'étoile se voit.",
        f"{M}|Le doudou a le droit d'être au dessin ?",
        f"{E}|Oui. Il a voyagé au jardin.",
        f"{N}|Mila pose le crayon. Un peu de vert à la pointe.",
        f"{N}|Le paillasson ne brille plus.",
        f"{P}|Nina verra le nuage, ou le soleil ?",
        f"{E}|Le nuage d'abord. C'est la surprise.",
    ), L(
        f"{N}|Au campement, un nuage denté entoure un soleil.",
        f"{N}|Le doudou montre une médaille verte, presque sèche.",
        f"{N}|Le crayon a une pointe un peu jardin.",
        f"{M}|La tache est devenue un nuage ?",
        f"{E}|Un ovale denté, plus une saleté.",
        f"{P}|La menthe vraie sèche, loin du tissu.",
        f"{N}|Un toc net, puis plus de dalle derrière la porte.",
        f"{E}|J'ai changé la tache en dessin.",
        f"{N}|Sur le verre, l'ovale tient la goutte comme un nid.",
        f"{N}|La médaille du doudou ne s'étend plus.",
    ), "crayon,tissu", "cacao,tissu", "crayon")

    add(2, 3, 2, L(
        f"{N}|La tasse est tiède. Le doudou a sa tache, à part.",
        f"{E}|Je bois. Toi, tu restes à côté, pas sur l'anse.",
        f"{N}|Mila boit. L'odeur de menthe et de savon se mêlent.",
        f"{N}|Son doigt tiède ferme le rond, sans toucher le doudou.",
        f"{P}|Tu as laissé le tissu au jardin, un peu ?",
        f"{E}|La tache, oui. Pas lui.",
        f"{N}|Le doudou s'assoit. La médaille verte est tournée vers le mur.",
        f"{N}|L'étoile bleue, elle, regarde la vitre.",
        f"{M}|Chacun sa face, c'est ça ?",
        f"{E}|Oui. Le vert sèche. Le bleu brille.",
        f"{N}|La goutte pose un point, loin de la tache.",
        f"{N}|Le toc est clair, sans tissu par-dessus.",
        f"{P}|Nina aura le doudou, le vert caché ?",
        f"{E}|Le vert contre moi. Le beige vers elle.",
    ), L(
        f"{N}|Au campement, le cacao sent la menthe et le savon.",
        f"{N}|Le doudou tourne sa médaille vers le mur, discrète.",
        f"{N}|Le soleil de doigt a un point, loin de tout vert.",
        f"{M}|L'étoile a regardé toute seule ?",
        f"{E}|Le bleu vers la vitre, le vert caché.",
        f"{P}|La feuille de menthe sèche, à l'écart du tissu.",
        f"{N}|Un toc clair, sans laine par-dessus.",
        f"{E}|J'ai bu, et le doudou a eu sa place.",
        f"{N}|Sur le verre, le point-goutte est loin de la tache.",
        f"{N}|Le beige du doudou redevient le plus visible.",
    ), "tasse,tissu", "cacao,tissu", "tasse")

    add(2, 3, 3, L(
        f"{N}|L'écharpe sent le jardin. Le doudou, la tache.",
        f"{E}|L'écharpe sur moi. Le doudou loin de l'anse.",
        f"{N}|Mila se couvre. Elle souffle un nuage, net.",
        f"{N}|Son doigt trace un rond. Puis un petit ovale, à part.",
        f"{P}|C'est la tache, l'ovale, plus loin ?",
        f"{E}|Oui. Pour qu'elle ait un dessin, elle aussi.",
        f"{N}|Le doudou s'assoit sous l'ovale, comme sous un toit.",
        f"{N}|L'étoile, libre, chauffe le grand soleil.",
        f"{M}|Deux dessins, deux tissus ?",
        f"{E}|Un pour Nina. Un pour le doudou.",
        f"{N}|La goutte choisit le grand soleil, et s'y couche.",
        f"{N}|Un toc net. L'écharpe tient les épaules.",
        f"{P}|Nina aura lequel ?",
        f"{E}|Le grand. Le petit, c'est le secret du doudou.",
    ), L(
        f"{N}|Au campement, deux ronds de buée se regardent.",
        f"{N}|L'écharpe sent le passage des gouttes, arrêté.",
        f"{N}|Le doudou s'abrite sous l'ovale, médaille cachée.",
        f"{M}|Le doudou a eu son soleil ?",
        f"{E}|Un petit rond, rien que pour lui.",
        f"{P}|La menthe sèche entre les deux dessins, en bas.",
        f"{N}|Un toc net, puis deux silences de laine.",
        f"{E}|J'ai soufflé pour deux.",
        f"{N}|Sur le verre, la goutte habite le plus grand rond.",
        f"{N}|L'ovale du doudou, lui, reste vide et fier.",
    ), "tissu,souffle", "cacao,tissu", "écharpe")

    # --- chambre + ballon ---
    add(3, 1, 1, L(
        f"{N}|Le crayon attend. Le fil de laine est dans la poche.",
        f"{E}|Je dessine le fil, autour du soleil, comme une écharpe.",
        f"{N}|Mila trace une spirale, lente, qui part de la goutte.",
        f"{N}|Le ballon, sous la chaise, n'a plus de fil au flanc.",
        f"{P}|Tu rends au verre ce que le ballon avait volé ?",
        f"{E}|Oui. Un fil pour le soleil. Pas pour rouler.",
        f"{N}|Le carré de laine tient l'anse, l'étoile dehors.",
        f"{N}|La spirale rencontre le trait brillant, et s'y noue.",
        f"{M}|C'est un nœud, ça, en haut ?",
        f"{E}|Un nœud de buée. Pour qu'il tienne.",
        f"{N}|La goutte s'arrête dans le nœud, comme dans une boucle.",
        f"{N}|Le toc est sourd, puis clair, sous le carré.",
        f"{P}|Nina suivra la spirale, tu crois ?",
        f"{E}|Jusqu'au nœud. C'est le bout du chemin.",
    ), L(
        f"{N}|Au campement, une spirale de buée noue un soleil.",
        f"{N}|Le ballon, sous la chaise, n'a plus de fil.",
        f"{N}|Le crayon a une pointe un peu laineuse, pour de faux.",
        f"{M}|Le fil est devenu un nœud ?",
        f"{E}|Une boucle de buée, en haut.",
        f"{P}|Le vrai fil dort dans ta poche, en boucle.",
        f"{N}|Un toc clair, sous le carré de laine.",
        f"{E}|J'ai donné un manteau au soleil.",
        f"{N}|Sur le verre, la goutte habite la boucle, sans glisser.",
        f"{N}|Le nid de la chambre, loin, s'est tu.",
    ), "crayon,tissu", "cacao,tissu", "crayon")

    add(3, 1, 2, L(
        f"{N}|La tasse est tiède, tenue dans le carré de laine.",
        f"{E}|Je bois. Le fil, lui, reste dans ma poche.",
        f"{N}|Mila boit. Le carré isole. L'étoile reste visible.",
        f"{N}|Son doigt tiède ferme le rond, sans le fil.",
        f"{P}|Le ballon a voulu tout couvrir. Toi, non ?",
        f"{E}|Non. Un coin d'anse, toujours.",
        f"{N}|Le ballon, sous la chaise, ne bouge plus.",
        f"{N}|Un fil, dans la poche, fait une petite boule.",
        f"{M}|Il a un nid, le fil, maintenant ?",
        f"{E}|Ma poche. Le soleil, la vitre.",
        f"{N}|La goutte pose un point, chaud comme le carré.",
        f"{N}|Le toc, sous la laine, est doux et juste.",
        f"{P}|Nina tiendra le carré, tu crois ?",
        f"{E}|Un bord. L'étoile, on la laisse dehors.",
    ), L(
        f"{N}|Au campement, le carré de laine est une anse molle.",
        f"{N}|Le ballon dort sous la chaise, sans fil.",
        f"{N}|Le soleil de doigt a un point chaud, beige pour de faux.",
        f"{M}|L'anse est restée visible ?",
        f"{E}|Un coin, malgré le chaud.",
        f"{P}|Le fil, dans ta poche, ne s'échappe plus.",
        f"{N}|Un toc doux, juste, sous la laine.",
        f"{E}|J'ai bu sans tout couvrir.",
        f"{N}|Sur le verre, le point-goutte a la couleur du carré.",
        f"{N}|L'oreiller de la chambre a gardé un creux, vide.",
    ), "tasse,tissu", "cacao,tissu", "tasse")

    add(3, 1, 3, L(
        f"{N}|L'écharpe et le carré se rencontrent, deux chauds.",
        f"{E}|L'écharpe sur moi. Le carré sous l'anse. Je souffle.",
        f"{N}|Mila noue. Un nuage neuf, large, couvre le trou du soleil.",
        f"{N}|Le fil de la poche ne sort pas. Le ballon reste sous la chaise.",
        f"{P}|Trois laines, et une seule pour le verre ?",
        f"{E}|Le souffle. Les laines, pour nous.",
        f"{N}|Son doigt trace des rayons, chauds des deux tissus.",
        f"{N}|L'étoile, entre écharpe et carré, fait un toc étouffé.",
        f"{M}|Elle a un manteau, l'anse, pas un cache-cache ?",
        f"{E}|Un manteau avec une fenêtre. L'étoile.",
        f"{N}|La goutte se couche dans un rayon, au chaud.",
        f"{N}|Le nid de la chambre semble plus loin.",
        f"{P}|Nina aura l'écharpe, ou le carré ?",
        f"{E}|L'écharpe un tour. Le carré, c'est la tasse.",
    ), L(
        f"{N}|Au campement, deux laines gardent un toc étouffé.",
        f"{N}|L'étoile bleue a une fenêtre, ronde, dans le tissu.",
        f"{N}|Le soleil de souffle est large, presque une couverture.",
        f"{M}|L'anse a eu une fenêtre ?",
        f"{E}|Une fenêtre ronde, pas un cache.",
        f"{P}|Le ballon, sous la chaise, n'a plus rien à voler.",
        f"{N}|Un toc étouffé, puis le silence des laines.",
        f"{E}|J'ai soufflé avec deux chauds.",
        f"{N}|Sur le verre, le rayon-goutte est le plus large.",
        f"{N}|Le fil, dans la poche, fait une boule sage.",
    ), "tissu,souffle", "cacao,tissu", "écharpe")

    # --- chambre + seau ---
    add(3, 2, 1, L(
        f"{N}|Le crayon attend. Le seau, vide, n'a plus de chausson.",
        f"{E}|Je dessine des mains, autour du soleil. Une par une.",
        f"{N}|Mila trace cinq doigts, puis cinq autres, dans la buée.",
        f"{N}|Le seau, posé, a assez de place, maintenant.",
        f"{P}|C'est tes mains, ça, trop pleines tout à l'heure ?",
        f"{E}|Oui. Une chose, puis l'autre. Voilà les mains libres.",
        f"{N}|Le carré de laine tient l'anse. Le crayon, l'autre main.",
        f"{N}|La goutte glisse entre deux doigts de buée, et s'arrête.",
        f"{M}|Elle a choisi un chemin, la goutte ?",
        f"{E}|Entre le pouce et l'index. Comme moi.",
        f"{N}|Le toc est net. Rien ne penche.",
        f"{N}|Le chausson, sous le lit, ne bouge plus.",
        f"{P}|Nina mettra sa main sur la tienne, sur le verre ?",
        f"{E}|À côté. Il y a de la place.",
    ), L(
        f"{N}|Au campement, deux mains de buée tiennent un soleil.",
        f"{N}|Le seau bleu, vide, a de la place, enfin.",
        f"{N}|Le crayon a tracé des doigts un peu trop grands.",
        f"{M}|Tes mains n'étaient plus trop pleines ?",
        f"{E}|Une chose, puis l'autre.",
        f"{P}|Le chausson dort sous le lit, à sa place.",
        f"{N}|Un toc net, rien qui penche.",
        f"{E}|J'ai dessiné le un par un.",
        f"{N}|Sur le verre, la goutte habite l'espace entre deux doigts.",
        f"{N}|La commode, loin, n'a plus la tasse.",
    ), "crayon,seau", "cacao,seau", "crayon")

    add(3, 2, 2, L(
        f"{N}|La tasse est tiède. Le seau, vide, devient table.",
        f"{E}|Un par un. Le seau. Le carré. Puis je bois.",
        f"{N}|Mila pose le seau. Puis le carré. Puis la tasse.",
        f"{N}|Trois tocs, de plus en plus petits, de plus en plus justes.",
        f"{P}|Tes mains ont appris l'ordre, là ?",
        f"{E}|Oui. Plus de chausson. Plus de trop-plein.",
        f"{N}|Elle boit. Son doigt tiède ferme le rond, libre.",
        f"{N}|L'étoile se voit. Le seau ne penche plus.",
        f"{M}|Le troisième toc, c'était le bon ?",
        f"{E}|Le plus petit. Le vrai.",
        f"{N}|La goutte pose un point, pile au troisième essai.",
        f"{N}|Le chausson, sous le lit, a perdu la partie.",
        f"{P}|Nina posera sa tasse, un par un, tu crois ?",
        f"{E}|Seau, carré, tasse. Je lui montrerai.",
    ), L(
        f"{N}|Au campement, trois étages : seau, laine, étoile.",
        f"{N}|Le soleil de doigt a un point, pile au centre.",
        f"{N}|La tasse étoilée a le toc le plus petit, le juste.",
        f"{M}|Les trois tocs étaient justes ?",
        f"{E}|De plus en plus vrais, un par un.",
        f"{P}|Le chausson n'est plus dans le seau.",
        f"{N}|Un dernier petit toc, puis le cacao.",
        f"{E}|J'ai mis l'ordre, pas la chambre.",
        f"{N}|Sur le verre, le point-goutte est au centre du rond.",
        f"{N}|La commode est vide, et ça va.",
    ), "tasse,seau", "cacao,seau", "tasse")

    add(3, 2, 3, L(
        f"{N}|L'écharpe attend. Le seau, vide, cale le pied du campement.",
        f"{E}|Je me couvre. Un par un. Puis je souffle.",
        f"{N}|Mila noue. Le seau tient le tapis, pour qu'il ne glisse pas.",
        f"{N}|Un nuage neuf. Des rayons. Rien dans les mains, pendant ce temps.",
        f"{P}|Le seau travaille en bas, toi en haut ?",
        f"{E}|Oui. Chacun son étage.",
        f"{N}|Le carré de laine reste sous l'anse, l'étoile dehors.",
        f"{N}|La goutte descend un rayon, sans se presser.",
        f"{M}|Tes mains, elles sont où, là ?",
        f"{E}|Sur l'écharpe. Plus dans le seau.",
        f"{N}|Un toc, puis le seau qui ne penche plus.",
        f"{N}|Le chausson, sous le lit, a compris.",
        f"{P}|Nina s'assoira sur le seau, tu crois ?",
        f"{E}|C'est trop petit. Elle aura le tapis.",
    ), L(
        f"{N}|Au campement, le seau cale le tapis, vide et sage.",
        f"{N}|L'écharpe tient Mila. Le carré tient l'anse.",
        f"{N}|Le soleil de souffle a des rayons, et des mains vides.",
        f"{M}|Tes mains n'avaient plus rien à rattraper ?",
        f"{E}|Libres, pendant que je soufflais.",
        f"{P}|Le chausson est rentré sous le lit, pour de bon.",
        f"{N}|Un toc, puis plus de bascule.",
        f"{E}|J'ai soufflé, les mains libres.",
        f"{N}|Sur le verre, la goutte a pris un rayon, sans chute.",
        f"{N}|Le pied du campement ne glisse plus.",
    ), "tissu,seau", "cacao,tissu", "écharpe")

    # --- chambre + doudou ---
    add(3, 3, 1, L(
        f"{N}|Le crayon attend. Le carré est sous l'anse. Le doudou à part.",
        f"{E}|Je dessine deux ronds. Le bon, et l'autre, plus petit.",
        f"{N}|Mila trace un grand soleil, puis un petit, à gauche.",
        f"{N}|Le petit a la taille du doudou, pour de faux.",
        f"{P}|C'est le mauvais beige, le petit, c'est ça ?",
        f"{E}|C'est lui. Il a le droit d'être là, pas sur l'anse.",
        f"{N}|La goutte choisit le grand, et s'y installe.",
        f"{N}|Le toc est net, sous le vrai carré.",
        f"{M}|Deux ronds, pour ne plus se tromper ?",
        f"{E}|Oui. Chacun sa place, sur le verre aussi.",
        f"{N}|Le nid de laine, loin, a l'air plus simple.",
        f"{N}|Le crayon a deux pointes de buée, presque.",
        f"{P}|Nina aura le grand, tu crois ?",
        f"{E}|Le grand. Le petit, c'est pour le doudou.",
    ), L(
        f"{N}|Au campement, deux soleils : le bon, et le petit à gauche.",
        f"{N}|Le doudou s'assoit sous le petit, sans toucher l'anse.",
        f"{N}|Le crayon a fini les deux ronds, sans se tromper.",
        f"{M}|Le mauvais beige a eu sa place ?",
        f"{E}|À part, sous son petit rond.",
        f"{P}|Le carré, lui, reste sous la vraie étoile.",
        f"{N}|Un toc net, du bon côté.",
        f"{E}|J'ai dessiné pour ne plus mêler les deux.",
        f"{N}|Sur le verre, la goutte habite le plus grand rond.",
        f"{N}|Le petit rond, vide, suffit au doudou.",
    ), "crayon,tissu", "cacao,tissu", "crayon")

    add(3, 3, 2, L(
        f"{N}|La tasse est tiède, dans le vrai carré, pas le doudou.",
        f"{E}|Je bois. Le doudou regarde, sans porter.",
        f"{N}|Mila boit. L'étoile se voit. Le doudou a les mains… rien.",
        f"{N}|Son doigt tiède ferme un seul rond, le bon.",
        f"{P}|Plus de deux beiges sur l'anse, c'est ça ?",
        f"{E}|Un seul. Le chaud. L'autre, ami, à côté.",
        f"{N}|Le doudou s'adosse au tapis, content d'être lui.",
        f"{N}|Le nid de la chambre n'a plus besoin de cacher.",
        f"{M}|Il a compris, le doudou ?",
        f"{E}|Il n'est pas un gant. Il est un ami.",
        f"{N}|La goutte pose un point, un seul, sous le bon rond.",
        f"{N}|Le toc est franc, sans tissu de trop.",
        f"{P}|Nina prendra le doudou, pas la tasse ?",
        f"{E}|Le doudou, pour attendre. La tasse, on partage.",
    ), L(
        f"{N}|Au campement, un seul rond de doigt, le bon.",
        f"{N}|Le doudou, ami, n'est plus un gant.",
        f"{N}|La tasse étoilée, dans le carré, a le toc franc.",
        f"{M}|Le doudou a eu le droit d'être lui ?",
        f"{E}|Un ami, plus un gant.",
        f"{P}|Le carré, lui, reste le gant de l'anse.",
        f"{N}|Un toc franc, sans double beige.",
        f"{E}|J'ai bu, et chacun avait son métier.",
        f"{N}|Sur le verre, un seul point-goutte, sous le bon soleil.",
        f"{N}|Le nid de laine, loin, est juste un nid.",
    ), "tasse,tissu", "cacao,tissu", "tasse")

    add(3, 3, 3, L(
        f"{N}|L'écharpe, le carré, le doudou : trois chauds, trois places.",
        f"{E}|Écharpe sur moi. Carré sous l'anse. Doudou à côté. Je souffle.",
        f"{N}|Mila noue. L'étoile reste une fenêtre. Le doudou ne touche pas.",
        f"{N}|Un nuage neuf. Un soleil. Un petit rond, cadeau, à gauche.",
        f"{P}|Trois métiers, et le souffle en plus ?",
        f"{E}|Oui. Personne sur les pieds de personne.",
        f"{N}|La goutte finit en sourire, au bas du grand soleil.",
        f"{N}|Trois tissus. Un toc. L'étoile, vue.",
        f"{M}|C'est le campement le plus plein, ça ?",
        f"{E}|Le plus clair, aussi.",
        f"{N}|Nina n'est pas là. Le sourire, lui, est prêt.",
        f"{N}|Le nid de la chambre peut attendre.",
        f"{P}|On lui montrera les trois places, tu crois ?",
        f"{E}|Oui. Chacun la sienne. Le verre, le nôtre.",
    ), L(
        f"{N}|Au campement, trois chauds, un sourire de goutte.",
        f"{N}|L'étoile bleue a sa fenêtre. Le doudou, son petit rond.",
        f"{N}|L'écharpe sent le cacao, et un peu la chambre.",
        f"{M}|Personne sur les pieds de personne ?",
        f"{E}|Trois places, et le verre à nous.",
        f"{P}|La tasse étoilée fume à peine, juste assez.",
        f"{N}|Un toc, puis le sourire qui ne glisse plus.",
        f"{E}|J'ai soufflé pour le grand, et laissé le petit.",
        f"{N}|Sur le verre, la goutte du début est un sourire, en bas.",
        f"{N}|Le campement tient, plein et clair, jusqu'à Nina.",
    ), "tissu,souffle", "cacao,tissu", "écharpe")

    return d


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> None:
        out[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "pluie-legere,cacao", {"emphasis": "tasse étoilée"})
    put(
        "CHK_T0001_P0000",
        L(
            f"{N}|Mila peut chercher d'abord dans trois pièces.",
            f"{M}|La cuisine, le jardin, ou la chambre ?",
        ),
        "choice",
        "",
        {"fields": {
            "option_1_label": "la cuisine",
            "option_2_label": "le jardin",
            "option_3_label": "la chambre",
        }},
    )

    for a, t1 in T1.items():
        put(f"CHK_T0001_P000{a}", t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        put(
            f"CHK_T0001_P000{a}_Q0001",
            t1["question"],
            "clue",
            "",
            {"night_policy": "skip", "fields": Q_FIELDS, "emphasis": "tasse"},
        )
        put(f"CHK_T0001_P000{a}_C0001", t1["confirm"], "confirm", "tasse,soucoupe", {"emphasis": "étoile"})
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            t1["t2q"],
            "choice",
            "",
            {"fields": {
                "option_1_label": "le ballon rouge",
                "option_2_label": "le seau bleu",
                "option_3_label": "le doudou",
            }},
        )

    t2 = t2_scenes()
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            lines, sons, emp = t2[(a, b)]
            cid = f"CHK_T0001_P000{a}_T0002_P000{b}"
            put(cid, lines, "obstacle", sons, {"emphasis": emp})
            put(
                f"{cid}_T0003_P0000",
                L(
                    f"{N}|{T3Q[(a, b)]}",
                    f"{P}|Le crayon, la tasse, ou l'écharpe ?",
                ),
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le crayon",
                    "option_2_label": "la tasse",
                    "option_3_label": "l'écharpe",
                }},
            )

    scenes = t3_end()
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                passage, ending, s3, se, emp = scenes[(a, b, c)]
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(base, passage, "resolution", s3, {"emphasis": emp})
                put(f"{base}_F0001", ending, "ending", se, {"emphasis": "goutte"})

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out]
    extra = sorted(set(out) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={extra[:8]}")

    ends = [out[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    t3_only = [
        out[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage"
        and "T0003_P000" in c["chunk_id"]
        and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    t2_only = [
        out[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "_T0002_P000" in c["chunk_id"] and "T0003" not in c["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Après la pluie, au campement de la vitre, Mila veut porter la tasse "
        "étoilée et dessiner un soleil dans la buée avant que la goutte arrive "
        "en bas. Nina vient. Il manque la cuillère, la menthe ou le carré. "
        "Première idée : dessiner sans la tasse. Ça rate. Elle la reprend. "
        "Ballon, seau ou doudou rusent plus fort. Crayon, tasse ou écharpe "
        "changent la manière de réussir. La goutte du début devient un rayon."
    )
    merged["title"] = TITLE
    merged["characters"] = "Mila, papa, maman"
    merged["setting"] = "salon, cuisine, jardin, chambre, vitre embuée"
    merged["chunks"] = [out[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3)
        for b in (1, 2, 3)
        for c in (1, 2, 3)
    ]
    if min(counts) < 550 or max(counts) > 700:
        raise SystemExit(f"chemins hors 550-700: {min(counts)}-{max(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    relecture(
        SID,
        TITLE,
        (
            "- **Public :** N2 (3–6 ans), audio familial\n"
            "- **Leçon :** AUT.AFF.003 — reprendre, vécue (la tasse étoilée ne "
            "sert le soleil que lorsque Mila revient la chercher)\n"
            "- **Personnages :** Mila, papa, maman (Nina attendue au goûter)\n"
            "- **Objet :** tasse étoilée (anse bleue, toc sur la soucoupe)\n"
            "- **Lieu nommé :** campement de la vitre, table du cacao, "
            "passage des gouttes, nid de laine\n"
            "- **Mission :** porter la tasse au carré de buée et y tracer un "
            "soleil avant que la goutte arrive en bas\n"
            "- **Déclencheur :** il manque la cuillère-étoile, la menthe ou "
            "le carré ; Nina n'est pas là\n"
            "- **1er imprévu :** dessiner sans la tasse, doigt froid, rond pâle\n"
            "- **2e ruse :** ballon (toc qui vole le glissement), seau (eau "
            "qui floute ou lave), doudou (étoile cachée / beige trompeur)\n"
            "- **Indice du début :** goutte-crayon ; la fin la transforme en rayon"
        ),
        (
            "Reprise F-NAR-019 P1. Noyau « La tasse de cacao et la vitre » "
            "conservé (salon, cuisine, jardin, chambre, vitre embuée). "
            "T1 ne retire pas l'équipement : la tasse reste au salon, Mila "
            "revient. Impatience, petit découragement, fierté calme. "
            "Adulte guide peu, pas de règle dite. Plus de tout doux / encore / "
            "déjà / tout calme. Un merci vécu (l'étoile visible). Question "
            "adulte. 27 fins, 27 T3, 9 T2 textuellement distincts. "
            "TTS : text_ssml, text_xai_tags, notes (arc, intention, émotion, "
            "intensité, destinataire, sous-texte, tempo, sourire, respiration), "
            "slow = choix / indice / fin. "
            f"N2 ≤ 15. Chemins {min(counts)}–{max(counts)} mots, "
            f"moy {sum(counts)//27}. check() OK. Pas d'apply."
        ),
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
