#!/usr/bin/env python3
"""TREE-AUT-002 — Le manteau du jardin gris (F-NAR-019, N2, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-AUT-002"
N2 = 15
TITLE = "Le manteau du jardin gris"
CHILD = "enfant-f"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|encore|déjà|deja)\b",
    re.I,
)
CLUE_BAD = (
    "ancre",
    "étoile brune",
    "fil pâle",
    "croissant d'eau",
    "croissant pâle",
    "virgule farine",
    "bouton nacre",
    "nœud raphia",
    "pois ivoire",
    "grain savon rose",
    "grain vanille",
    "pastille colle",
    "virgule buée",
    "capuchon penche",
    "grain doré",
    "brin safran",
    "anneau liège",
    "clou tête ronde",
    "grain d'ambre",
    "goutte de cire rouge",
    "anneau de zinc",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "anneau de pollen",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille d'étain",
    "vis verte",
    "cristal de sucre brun",
    "écaille de lichen",
    "grain de cire claire",
    "dent de fermeture dorée",
    "écaille de nacre",
    "grain de paprika",
    "écaille de boue blonde",
    "point de rouille",
    "grain de mica",
    "grain de cannelle",
    "grain d'ocre",
    "grain de feutre",
    "grain de sésame",
    "écaille de savon",
    "grain de suie",
    "grain de limon",
    "grain de quartz",
    "grain de sel",
    "grain de lessive",
    "grain de cerise",
    "rond d'huile",
    "écaille d'orange",
    "point d'écume",
    "grain de sève",
    "point de beurre",
    "grain de craie",
    "grain de pomme",
    "grain de bitume",
    "grain de laine",
    "grain de grelot",
    "grain de parquet",
    "trait de craie",
    "grain de lavande",
    "merle",
    "couleur de miel",
    "j'ai compris",
    "mission accomplie",
    "aujourd'hui,",
    "gouttes au bord",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de terre grise",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=2; destinataire=enfant; sous_texte=le_grain_attend_sur_le_crochet; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_sortie; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="manteau",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=elle_est_revenue_le_chercher; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="crochet",
        note="arc=confirmation; intention=relancer; emotion=élan_prudent; intensite=1; destinataire=enfant; sous_texte=le_manteau_part_avec_elle; tempo=naturel; sourire=léger; respiration=fluide",
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
        emphasis="grain de terre grise",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=elle_accroche_sans_foncer; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="crochet",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_a_paye_le_crochet; tempo=posé; sourire=léger; respiration=ample",
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": (
        "manteau | le manteau | son manteau | prendre manteau | "
        "le rouge | le bleu | le vert | manteau rouge | manteau bleu | manteau vert"
    ),
    "retry_prompt": "Elle a pris le manteau. Sarah a pris quoi ?",
    "engine_ok_text": "Oui, elle a pris le manteau.",
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
        for bad in CLUE_BAD:
            if bad in low:
                raise SystemExit(f"indice/refrain {bad}: {ph}")
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
    f"{N}|Les chaussures d'été rentrent dans le carton.",
    f"{P}|Elles ont fini, Sarah.",
    f"{N}|Une botte d'automne tape la marche.",
    f"{N}|Un grain de terre grise saute, puis se pose.",
    f"{N}|Il tient sur le crochet bas, minuscule.",
    f"{N}|Sarah le voit, et ne sait pas.",
    f"{N}|L'air de l'entrée sent le bois mouillé.",
    f"{N}|Derrière la vitre, le jardin est gris.",
    f"{N}|Le banc aux feuilles porte des timbres mouillés.",
    f"{E}|Je veux les feuilles, avant le vent !",
    f"{M}|Tu as vu le banc, tout mouillé ?",
    f"{E}|Oui, maman.",
    f"{E}|Je cours.",
    f"{N}|En ce moment, Sarah court vers la porte.",
    f"{N}|Trois manteaux pendent : rouge, bleu, vert.",
    f"{P}|Le vent n'attend pas.",
    f"{E}|Le banc m'attend !",
)

T1 = {
    1: {
        "sons": "porte,tissu",
        "emphasis": "manteau rouge",
        "passage": L(
            f"{N}|Sarah tire le manteau rouge du crochet.",
            f"{N}|Une manche est à l'envers, toute molle.",
            f"{E}|Je n'ai pas le temps !",
            f"{N}|Elle jette le rouge sur la chaise.",
            f"{N}|Papa ouvre un peu la porte.",
            f"{N}|L'air entre, froid comme de l'eau.",
            f"{E}|Aïe, mes bras !",
            f"{N}|Le sourire de Sarah disparaît.",
            f"{M}|Maman s'accroupit, à la même hauteur.",
            f"{M}|Tu veux le rouge, Sarah ?",
            f"{E}|Oui. Il est chaud.",
            f"{N}|Elle pousse un bras. La manche résiste.",
            f"{P}|Un bras, puis l'autre.",
            f"{N}|Sarah ralentit. Le rouge monte, enfin.",
            f"{N}|Un grain de terre grise tombe de la poche.",
            f"{E}|Toi, tu viens aussi.",
        ),
        "question": L(
            f"{N}|L'air était froid. Sarah est revenue.",
            f"{M}|Elle est revenue chercher quoi ?",
        ),
        "confirm": L(
            f"{N}|Sarah ramasse le grain, le remet dans la poche.",
            f"{N}|Le manteau rouge est fermé, bien chaud.",
            f"{M}|Merci, je vois tes mains au chaud.",
            f"{P}|On va au banc aux feuilles ?",
            f"{E}|Oui, papa. Avec le rouge.",
            f"{N}|Le crochet bas reste vide, un instant.",
            f"{N}|La botte d'automne garde une trace ronde.",
            f"{M}|Tu emportes un jeu, pour le banc ?",
            f"{E}|Oui. Pour les feuilles.",
            f"{N}|Ils passent la porte. Le jardin sent la terre.",
        ),
        "t2q": L(
            f"{N}|Un jeu peut aider au banc aux feuilles.",
            f"{P}|Le ballon rouge, le seau bleu, ou le doudou ?",
        ),
    },
    2: {
        "sons": "porte,boutons",
        "emphasis": "manteau bleu",
        "passage": L(
            f"{N}|Sarah passe devant le manteau bleu.",
            f"{N}|Les boutons sont gros, ronds, un peu froids.",
            f"{E}|Le banc m'attend !",
            f"{N}|Elle pousse la porte, sans le bleu.",
            f"{N}|L'air pique les joues, puis les mains.",
            f"{E}|Il fait froid.",
            f"{N}|Le sourire disparaît. Ses épaules se serrent.",
            f"{M}|Tu reviens, Sarah ?",
            f"{N}|Sarah revient vers le crochet.",
            f"{N}|Elle tire trop vite. Un bouton refuse.",
            f"{E}|Je n'y arrive pas.",
            f"{N}|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            f"{P}|Papa s'accroupit, près du crochet.",
            f"{N}|Sarah prend le bleu, bouton après bouton.",
            f"{N}|Sur le poignet, un grain de terre grise tient.",
            f"{E}|On va au jardin gris.",
        ),
        "question": L(
            f"{N}|L'air était froid. Sarah est revenue.",
            f"{P}|Elle est revenue chercher quoi ?",
        ),
        "confirm": L(
            f"{N}|Les boutons du bleu tiennent, un par un.",
            f"{N}|Sarah souffle dans ses mains, au chaud.",
            f"{M}|Merci, je vois tes mains au chaud.",
            f"{P}|On va au banc aux feuilles ?",
            f"{E}|Oui. Avec le bleu.",
            f"{N}|Le crochet bas reste vide, un instant.",
            f"{N}|Le capuchon tape, mol, contre son dos.",
            f"{M}|Tu emportes un jeu, pour le banc ?",
            f"{E}|Oui. Pour les feuilles.",
            f"{N}|Ils passent la porte. Le jardin sent la terre.",
        ),
        "t2q": L(
            f"{N}|Un jeu peut aider au banc aux feuilles.",
            f"{M}|Le ballon rouge, le seau bleu, ou le doudou ?",
        ),
    },
    3: {
        "sons": "marche,tissu",
        "emphasis": "manteau vert",
        "passage": L(
            f"{N}|Sarah prend le manteau vert, trop long.",
            f"{N}|Une feuille sèche colle au tissu.",
            f"{E}|J'enlève la feuille.",
            f"{N}|Elle pose le vert sur la marche.",
            f"{N}|Puis elle court vers le banc aux feuilles.",
            f"{N}|L'air froid lui serre les épaules.",
            f"{E}|Mon dos a froid.",
            f"{P}|Le vert est resté sur la marche.",
            f"{N}|Sarah revient. Ses mains tremblent un peu.",
            f"{N}|Elle glisse les manches, trop vite. Le bas traîne.",
            f"{M}|Maman se baisse, à sa hauteur.",
            f"{M}|Le capuchon, si tu veux ?",
            f"{N}|Sarah met le capuchon, sans se presser.",
            f"{N}|Au bas de l'ourlet, un grain de terre grise tient.",
            f"{E}|Avec le vert, maintenant.",
        ),
        "question": L(
            f"{N}|L'air était froid. Sarah est revenue.",
            f"{M}|Elle est revenue chercher quoi ?",
        ),
        "confirm": L(
            f"{N}|Le capuchon vert tient chaud aux oreilles.",
            f"{N}|Sarah soulève un peu l'ourlet, pour marcher.",
            f"{M}|Merci, je vois tes mains au chaud.",
            f"{P}|On va au banc aux feuilles ?",
            f"{E}|Oui. Avec le vert.",
            f"{N}|Le crochet bas reste vide, un instant.",
            f"{N}|La marche garde un carré de tissu, un moment.",
            f"{M}|Tu emportes un jeu, pour le banc ?",
            f"{E}|Oui. Pour les feuilles.",
            f"{N}|Ils passent la porte. Le jardin sent la terre.",
        ),
        "t2q": L(
            f"{N}|Un jeu peut aider au banc aux feuilles.",
            f"{P}|Le ballon rouge, le seau bleu, ou le doudou ?",
        ),
    },
}


def t2_scenes() -> dict[tuple[int, int], tuple]:
    data: dict[tuple[int, int], tuple] = {}
    data[(1, 1)] = (
        L(
            f"{N}|Le ballon rouge attend près du banc aux feuilles.",
            f"{N}|Une flaque lui fait un miroir gris.",
            f"{E}|Toi aussi, au banc !",
            f"{N}|Sarah le lance. Il file sous le bois.",
            f"{N}|Elle rampe. La manche rouge s'accroche.",
            f"{N}|Une écharde tient le tissu, serrée.",
            f"{E}|Lâche-moi !",
            f"{N}|Elle tire trop fort. La manche reste.",
            f"{N}|Le sourire de Sarah disparaît.",
            f"{N}|Un grain de terre grise tombe du poignet.",
            f"{P}|Papa s'accroupit, à la même hauteur.",
            f"{P}|Tu le poses où, le rouge ?",
            f"{E}|Je ne sais pas. Ça serre, là.",
            f"{N}|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            f"{E}|Je ne fonce pas.",
            f"{N}|Elle écoute le bois mouillé, tout près.",
        ),
        "ballon,bois",
        "ballon",
    )
    data[(1, 2)] = (
        L(
            f"{N}|Le seau bleu attend près des feuilles mouillées.",
            f"{E}|Je les ramène, pour la table !",
            f"{N}|Sarah ramasse trop vite. Le seau penche.",
            f"{N}|Le manteau rouge glisse d'une épaule.",
            f"{N}|Les feuilles tombent sur le tissu, froides.",
            f"{E}|Il est trop lourd !",
            f"{N}|Elle veut tout porter. Le seau bascule.",
            f"{N}|L'eau grise mouille la poche.",
            f"{N}|Ses épaules baissent.",
            f"{N}|Au fond du seau, le grain de terre grise brille.",
            f"{M}|Maman se baisse, face à elle.",
            f"{M}|Tu poses le seau, d'abord ?",
            f"{E}|D'abord le seau. Pas tout.",
            f"{N}|Sarah refuse de foncer.",
            f"{N}|Elle écoute le jardin, sans bouger.",
        ),
        "seau,feuilles",
        "seau",
    )
    data[(1, 3)] = (
        L(
            f"{N}|Le doudou attend sur le banc mouillé.",
            f"{E}|Tu viens, au chaud !",
            f"{N}|Sarah l'enroule dans le manteau rouge.",
            f"{N}|Le doudou est au sec. Le manteau, non.",
            f"{N}|Le rouge reste sur le bois, oublié.",
            f"{E}|Oh. Je l'ai laissé.",
            f"{N}|Elle veut le prendre d'un coup. Le banc glisse.",
            f"{N}|Le sourire s'en va.",
            f"{N}|Sur l'oreille du doudou, le grain de terre grise tient.",
            f"{P}|Papa s'accroupit, à la même hauteur.",
            f"{P}|Le manteau, ou le doudou, d'abord ?",
            f"{E}|Le manteau. Il a froid, lui.",
            f"{N}|Cette fois, Sarah ne court pas.",
            f"{N}|Elle écoute le bois mouillé.",
            f"{N}|Le doudou attend, l'oreille grise tournée.",
        ),
        "tissu,banc",
        "doudou",
    )
    data[(2, 1)] = (
        L(
            f"{N}|Le ballon rouge roule vers les boutons bleus.",
            f"{E}|Attrape, ballon !",
            f"{N}|Le ballon tape un bouton. Le bleu s'ouvre.",
            f"{N}|Sarah court après lui. Le capuchon saute.",
            f"{N}|Elle veut boutonner en courant. Les doigts glissent.",
            f"{E}|Ils ne veulent pas !",
            f"{N}|L'air froid entre dans le bleu, vite.",
            f"{N}|Cette fois, Sarah ne rit plus.",
            f"{N}|Un grain de terre grise brille dans une boutonnière.",
            f"{M}|Maman se baisse, à sa hauteur.",
            f"{M}|Tu t'arrêtes, ou tu cours ?",
            f"{E}|Je m'arrête. Les boutons d'abord.",
            f"{N}|Sarah refuse de foncer.",
            f"{N}|Elle écoute le ballon, qui se tait dans l'herbe.",
        ),
        "ballon,boutons",
        "ballon",
    )
    data[(2, 2)] = (
        L(
            f"{N}|Sarah pose le seau bleu près des boutons.",
            f"{N}|Une feuille tombe dedans, trop lourde.",
            f"{E}|Encore une, pour la table.",
        ),
        "seau,boutons",
        "seau",
    )
    data[(2, 3)] = (
        L(
            f"{N}|Le doudou voyage dans la manche du bleu.",
            f"{N}|Sarah arrive au banc, une oreille qui dépasse.",
            f"{E}|Tu regardes les feuilles avec moi !",
            f"{N}|Le capuchon bascule. Le doudou tombe dans la flaque.",
            f"{E}|Il est mouillé !",
            f"{N}|Elle jette le bleu par terre, pour le sécher.",
            f"{N}|Le manteau boit la terre grise, trop vite.",
            f"{N}|Ses mains se ferment, vides.",
            f"{N}|Le grain de terre grise quitte le poignet, perdu.",
            f"{P}|Papa s'accroupit, près de la flaque.",
            f"{P}|Le bleu, ou le doudou, d'abord ?",
            f"{E}|Le bleu. Il boit la terre.",
            f"{N}|Dans sa poitrine, ça se bouscule.",
            f"{N}|Sarah refuse de foncer.",
            f"{N}|Elle écoute l'eau de la flaque, trop plate.",
        ),
        "tissu,flaque",
        "doudou",
    )
    data[(3, 1)] = (
        L(
            f"{N}|Le manteau vert frotte les feuilles, trop long.",
            f"{N}|Le ballon rouge part trop loin.",
            f"{E}|Reviens !",
            f"{N}|Sarah donne un coup de pied. L'ourlet s'accroche.",
            f"{N}|Elle tombe assise. Le vert mange la terre.",
            f"{E}|Je suis trop grande, non. Lui est trop long.",
            f"{N}|Le sourire disparaît. L'ourlet est lourd de boue.",
            f"{N}|Le grain de terre grise, sur l'ourlet, a un frère.",
            f"{M}|Maman se baisse, face à elle.",
            f"{M}|Tu te relèves, sans tirer ?",
            f"{E}|Sans tirer. Doucement, l'ourlet.",
            f"{N}|Sarah refuse de foncer.",
            f"{N}|Elle écoute le ballon, arrêté contre une pierre.",
            f"{N}|Deux grains, presque pareils, tiennent au bas.",
        ),
        "ballon,ourlet",
        "ballon",
    )
    data[(3, 2)] = (
        L(
            f"{N}|Sarah traîne le seau, et le vert touche la terre.",
            f"{N}|Des feuilles dépassent, trop hautes.",
            f"{E}|Je le porte, comme papa !",
            f"{N}|L'anse s'enroule dans l'ourlet. Sarah ne peut plus marcher.",
            f"{N}|Elle tire fort. Le seau se vide, d'un coup.",
            f"{E}|Mes feuilles !",
            f"{N}|Ses épaules tombent. Le jardin a tout repris.",
            f"{N}|Au fond du seau, le grain de terre grise reste.",
            f"{P}|Papa s'accroupit, à la même hauteur.",
            f"{P}|L'ourlet d'abord, ou le seau ?",
            f"{E}|L'ourlet. Après, le seau.",
            f"{N}|Sarah refuse de foncer.",
            f"{N}|Elle écoute les feuilles, collées au bois du banc.",
            f"{N}|L'anse, libre, penche, vide.",
        ),
        "seau,ourlet",
        "seau",
    )
    data[(3, 3)] = (
        L(
            f"{N}|Le doudou voyage sous le capuchon vert.",
            f"{N}|Sarah arrive au banc, une oreille cachée.",
            f"{E}|On s'assoit, tous les deux !",
            f"{N}|Le capuchon trop long cache le doudou, tombé.",
            f"{N}|Elle cherche partout. Pas sous le vert.",
            f"{E}|Il a disparu.",
            f"{N}|Le sourire s'en va. Ses mains fouillent l'herbe.",
            f"{N}|Personne ne donne la réponse.",
            f"{M}|Maman se baisse, sans montrer.",
            f"{M}|Tu as regardé le capuchon ?",
            f"{E}|Pas encore. Attends.",
        ),
        "tissu,capuchon",
        "doudou",
    )
    return data


# (2,2) and (3,3) T2 were truncated to avoid "encore" — fix (2,2) fully and (3,3).
# Rewrite those two here after seeing the tic in (3,3) "Pas encore".


def t2_scenes_fixed() -> dict[tuple[int, int], tuple]:
    data = t2_scenes()
    data[(2, 2)] = (
        L(
            f"{N}|Sarah pose le seau bleu près des boutons.",
            f"{N}|Une feuille tombe dedans, trop lourde.",
            f"{E}|Une autre, pour la table !",
            f"{N}|L'anse accroche un bouton bleu, net.",
            f"{N}|Le manteau part vers la flaque, tiré.",
            f"{E}|Lâche le bouton !",
            f"{N}|Elle tire. Le bouton presque saute.",
            f"{N}|Le sourire disparaît. Un fil blanc tient, mince.",
            f"{N}|Dans l'eau du seau, le grain de terre grise tourne.",
            f"{M}|Maman se baisse, face à elle.",
            f"{M}|Tu décroches lentement, tu crois ?",
            f"{E}|Lentement. Pas d'un coup.",
            f"{N}|Sarah refuse de foncer.",
            f"{N}|Elle écoute le fil, trop tendu.",
            f"{N}|Le seau penche, puis s'arrête.",
        ),
        "seau,boutons",
        "seau",
    )
    data[(3, 3)] = (
        L(
            f"{N}|Le doudou voyage sous le capuchon vert.",
            f"{N}|Sarah arrive au banc, une oreille cachée.",
            f"{E}|On s'assoit, tous les deux !",
            f"{N}|Le capuchon trop long cache le doudou, tombé.",
            f"{N}|Elle cherche partout. Pas sous le vert.",
            f"{E}|Il a disparu.",
            f"{N}|Le sourire s'en va. Ses mains fouillent l'herbe.",
            f"{N}|Personne ne donne la réponse.",
            f"{M}|Maman se baisse, sans montrer.",
            f"{M}|Tu as regardé le capuchon ?",
            f"{E}|Pas celui-là. J'ai regardé l'herbe.",
            f"{N}|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            f"{N}|Sarah refuse de foncer.",
            f"{N}|Elle écoute le tissu, trop silencieux.",
            f"{N}|Un grain de terre grise brille au bord du capuchon.",
        ),
        "tissu,capuchon",
        "doudou",
    )
    return data


T3Q = {
    (1, 1): "Le ballon a volé la manche. Ensuite ?",
    (1, 2): "Le seau a mouillé la poche. Ensuite ?",
    (1, 3): "Le doudou a gardé le rouge. Ensuite ?",
    (2, 1): "Le ballon a ouvert les boutons. Ensuite ?",
    (2, 2): "L'anse a tiré le bouton. Ensuite ?",
    (2, 3): "Le bleu a bu la terre. Ensuite ?",
    (3, 1): "L'ourlet a mangé la terre. Ensuite ?",
    (3, 2): "L'anse a noué l'ourlet. Ensuite ?",
    (3, 3): "Le capuchon a caché le doudou. Ensuite ?",
}


def t3_end() -> dict[tuple[int, int, int], tuple]:
    d: dict[tuple[int, int, int], tuple] = {}

    def add(a, b, c, passage, ending, s3, se, emp):
        d[(a, b, c)] = (passage, ending, s3, se, emp)

    add(1, 1, 1, L(
        f"{N}|Un chat gris s'assoit sur le manteau rouge.",
        f"{N}|Sa patte joue avec le grain de terre grise.",
        f"{E}|C'est à moi, le rouge.",
        f"{N}|Sarah veut le tirer. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Personne ne donne la réponse.",
        f"{N}|Elle observe le rouge, écoute le ronron.",
        f"{P}|Il va partir, tu crois ?",
        f"{E}|S'il veut. Je reste.",
        f"{N}|Le chat saute. Le grain reste sur la poche.",
        f"{N}|Sarah reprend le rouge, sans le secouer.",
        f"{M}|Le crochet, là-bas, est vide.",
        f"{N}|Elle rentre. Le grain voyage dans la poche.",
        f"{N}|Le rouge retrouve le crochet bas, d'un clic.",
    ), L(
        f"{N}|Dans l'entrée, le crochet a son manteau rouge.",
        f"{N}|Le grain de terre grise brille dans la poche.",
        f"{N}|Un poil gris reste au col, minuscule.",
        f"{M}|Tu as vu le poil ?",
        f"{E}|Le chat a gardé une place.",
        f"{P}|Le ballon sèche près des chaussures.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai raccroché, toute seule.",
        f"{N}|Derrière la vitre, le banc aux feuilles attend, vide.",
        f"{N}|Le clic du crochet tient, net, dans le bois.",
    ), "chat,manteau", "crochet,bois", "grain de terre grise")

    add(1, 1, 2, L(
        f"{N}|Un chien brun prend la manche rouge, gentiment.",
        f"{N}|Il tire vers la haie, trop content.",
        f"{E}|Non, pas la haie.",
        f"{N}|Sarah veut courir. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle parle bas, sans tirer.",
        f"{P}|Il t'écoute, tu crois ?",
        f"{E}|S'il lâche. Je reste là.",
        f"{N}|Le chien pose la manche. Le grain tombe dans l'herbe.",
        f"{N}|Sarah ramasse le grain, puis le rouge.",
        f"{M}|Le crochet, lui, n'a rien tiré.",
        f"{N}|Elle rentre. Le grain revient vers le bois.",
        f"{N}|Le rouge retrouve le crochet bas, d'un clic.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, la manche un peu mâchée.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une trace de patte sèche près du paillasson.",
        f"{M}|Tu as vu la patte ?",
        f"{E}|Le chien a voulu la haie.",
        f"{P}|Le ballon a une marque de dents, petite.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai parlé, sans tirer.",
        f"{N}|Derrière la vitre, la haie ne bouge plus.",
        f"{N}|Le clic du crochet tient, plus grave.",
    ), "chien,manche", "crochet,paillasson", "grain de terre grise")

    add(1, 1, 3, L(
        f"{N}|Une poule picore le poignet du rouge.",
        f"{N}|Elle a vu le grain de terre grise, net.",
        f"{E}|C'est pas une graine.",
        f"{N}|Sarah veut chasser la poule. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le bec, écoute le jardin.",
        f"{M}|Elle va le prendre, tu crois ?",
        f"{E}|Peut-être. Je regarde.",
        f"{N}|La poule saisit le grain, fait un pas, le pose.",
        f"{N}|Le grain est près du chemin de l'entrée.",
        f"{N}|Sarah suit, le rouge sur le bras.",
        f"{P}|Le crochet n'est pas loin.",
        f"{N}|Elle raccroche. Le grain retrouve le bois.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, un trou de bec au poignet.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume grise reste sous la chaise.",
        f"{M}|Tu as vu la plume ?",
        f"{E}|La poule a cru à une graine.",
        f"{P}|Le ballon a une trace de terre, ronde.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai suivi, sans crier.",
        f"{N}|Derrière la vitre, la poule picore ailleurs.",
        f"{N}|Le clic du crochet tient, léger.",
    ), "poule,grain", "crochet,plume", "grain de terre grise")

    add(1, 2, 1, L(
        f"{N}|Un chat gris s'assoit dans le seau de feuilles.",
        f"{N}|Le manteau rouge reste par terre, trop près.",
        f"{E}|C'est mon seau.",
        f"{N}|Sarah veut le soulever. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le seau, écoute le ronron.",
        f"{P}|Il va sauter, tu crois ?",
        f"{E}|S'il veut. Le rouge attend.",
        f"{N}|Le chat saute. Au fond, le grain de terre grise brille.",
        f"{N}|Sarah reprend le rouge, puis le grain.",
        f"{M}|Le crochet, lui, n'a pas de chat.",
        f"{N}|Elle rentre. Le seau reste vide, près du banc.",
        f"{N}|Le rouge retrouve le crochet bas, d'un clic.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, une feuille collée à la poche.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Un poil gris reste dans le seau, au sec.",
        f"{M}|Tu as vu le poil ?",
        f"{E}|Le chat a choisi les feuilles.",
        f"{P}|Le seau bleu sèche près du paillasson.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai attendu, puis j'ai pris.",
        f"{N}|Derrière la vitre, le seau garde sa feuille.",
        f"{N}|Le clic du crochet tient, net.",
    ), "chat,seau", "crochet,seau", "grain de terre grise")

    add(1, 2, 2, L(
        f"{N}|Un chien brun renifle le seau, trop curieux.",
        f"{N}|Le seau bascule. L'ourlet rouge boit l'eau.",
        f"{E}|Arrête !",
        f"{N}|Sarah veut tirer le rouge. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle soulève le tissu, lentement, loin du nez.",
        f"{P}|Il est lourd, maintenant ?",
        f"{E}|Lourd d'eau. Je le porte comme ça.",
        f"{N}|Le grain de terre grise tient à l'ourlet mouillé.",
        f"{N}|Sarah rentre, le rouge à deux mains.",
        f"{M}|Le crochet aime le sec, un peu.",
        f"{N}|Elle égoutte. Puis le clic, sur le bois.",
        f"{N}|Le grain, lui, revient au crochet, plus foncé.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, l'ourlet plus sombre.",
        f"{N}|Le grain de terre grise sèche sur le crochet.",
        f"{N}|L'eau quitte le tissu, puis plus rien.",
        f"{M}|Tu as vu l'ourlet ?",
        f"{E}|Le chien a versé. J'ai porté.",
        f"{P}|Le seau bleu a une dent, sur le bord.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai soulevé, sans tirer.",
        f"{N}|Derrière la vitre, le banc brille, sans seau.",
        f"{N}|Le clic du crochet tient, un peu mouillé.",
    ), "chien,seau", "crochet,eau", "grain de terre grise")

    add(1, 2, 3, L(
        f"{N}|Une poule picore les feuilles du seau.",
        f"{N}|Au fond, le grain de terre grise l'intéresse.",
        f"{E}|C'est pas pour toi.",
        f"{N}|Sarah veut couvrir le seau. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le bec, écoute le gravier.",
        f"{M}|Elle va le sortir, tu crois ?",
        f"{E}|Peut-être. Je la laisse chercher.",
        f"{N}|La poule sort le grain, le pose vers la porte.",
        f"{N}|Sarah prend le rouge, suit le grain.",
        f"{P}|Le crochet n'est pas loin.",
        f"{N}|Elle raccroche. Le grain retrouve le bois.",
        f"{N}|Le seau, vide, reste au jardin.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, une nervure de feuille au col.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume reste dans le seau, au seuil.",
        f"{M}|Tu as vu la plume ?",
        f"{E}|La poule a trouvé le grain.",
        f"{P}|Le seau bleu garde une feuille, toute plate.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai suivi le bec, sans crier.",
        f"{N}|Derrière la vitre, plus de feuilles dans le seau.",
        f"{N}|Le clic du crochet tient, sec.",
    ), "poule,seau", "crochet,feuille", "grain de terre grise")

    add(1, 3, 1, L(
        f"{N}|Un chat gris pétrit le doudou, dans le rouge.",
        f"{N}|Le manteau est un nid, trop bon.",
        f"{E}|C'est pas un lit.",
        f"{N}|Sarah veut le dégager. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe les pattes, écoute le ronron.",
        f"{P}|Il va se lasser, tu crois ?",
        f"{E}|S'il a assez pétrí. Je reste.",
        f"{N}|Le chat part. Sur l'oreille, le grain de terre grise tient.",
        f"{N}|Sarah reprend le rouge. Le doudou à part.",
        f"{M}|Le crochet n'est pas un nid.",
        f"{N}|Elle rentre. Le rouge retrouve le bois, d'un clic.",
        f"{N}|Le grain voyage, collé à l'oreille, puis au crochet.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, un pli de nid au milieu.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Le doudou garde un poil gris, sur l'oreille.",
        f"{M}|Tu as vu le poil ?",
        f"{E}|Le chat a cru à un nid.",
        f"{P}|Le doudou sèche sur la chaise, à part.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai attendu la fin du ronron.",
        f"{N}|Derrière la vitre, le banc n'a plus de nid.",
        f"{N}|Le clic du crochet tient, feutré.",
    ), "chat,doudou", "crochet,tissu", "grain de terre grise")

    add(1, 3, 2, L(
        f"{N}|Un chien brun emporte le doudou. Le rouge suit.",
        f"{N}|Les deux glissent vers la haie, ensemble.",
        f"{E}|Revenez, les deux.",
        f"{N}|Sarah veut courir. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle appelle, sans tirer.",
        f"{P}|Il t'entend, tu crois ?",
        f"{E}|S'il ramène. Je reste au banc.",
        f"{N}|Le chien revient. Le grain de terre grise est dans la doublure.",
        f"{N}|Sarah sépare le rouge et le doudou.",
        f"{M}|Chacun sa place, là.",
        f"{N}|Elle rentre. Le rouge retrouve le crochet, d'un clic.",
        f"{N}|Le grain, de la doublure, revient au bois.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, la doublure un peu tournée.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Le doudou a une odeur de chien, légère.",
        f"{M}|Tu as senti le doudou ?",
        f"{E}|Le chien a voulu les deux.",
        f"{P}|Le doudou sèche, loin de la haie.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai appelé, sans courir.",
        f"{N}|Derrière la vitre, la haie n'a plus rien.",
        f"{N}|Le clic du crochet tient, franc.",
    ), "chien,doudou", "crochet,tissu", "grain de terre grise")

    add(1, 3, 3, L(
        f"{N}|Une poule picore le bouton du doudou.",
        f"{N}|Le grain de terre grise est juste à côté.",
        f"{E}|C'est un bouton, pas une graine.",
        f"{N}|Sarah veut éloigner le doudou. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le bec, écoute le jardin.",
        f"{M}|Elle va tout mélanger, tu crois ?",
        f"{E}|Peut-être. Je sépare après.",
        f"{N}|La poule laisse le bouton. Le grain roule vers la porte.",
        f"{N}|Sarah prend le rouge, le doudou à l'autre main.",
        f"{P}|Le crochet, pour le rouge seulement.",
        f"{N}|Elle raccroche. Le grain retrouve le bois.",
        f"{N}|Le doudou, lui, va sur la chaise.",
    ), L(
        f"{N}|Dans l'entrée, le rouge pend, loin du doudou.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Le bouton du doudou a une trace de bec.",
        f"{M}|Tu as vu le bouton ?",
        f"{E}|La poule a tout mêlé.",
        f"{P}|Le doudou sèche sur la chaise, à part.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai séparé, sans crier.",
        f"{N}|Derrière la vitre, plus de bouton dans l'herbe.",
        f"{N}|Le clic du crochet tient, seul.",
    ), "poule,doudou", "crochet,chaise", "grain de terre grise")

    add(2, 1, 1, L(
        f"{N}|Un chat gris tape le ballon, puis le capuchon bleu.",
        f"{N}|Le capuchon tombe. Le grain de terre grise brille dedans.",
        f"{E}|Rends le capuchon.",
        f"{N}|Sarah veut le reprendre d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le capuchon, écoute le ronron.",
        f"{P}|Il va s'ennuyer, tu crois ?",
        f"{E}|S'il n'a plus le ballon. Je reste.",
        f"{N}|Le chat part. Sarah ramasse le capuchon, le grain.",
        f"{N}|Elle boutonne, un par un, sans courir.",
        f"{M}|Le crochet aime les boutons fermés.",
        f"{N}|Elle rentre. Le bleu retrouve le bois, d'un clic.",
        f"{N}|Le grain, du capuchon, revient au crochet.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, le capuchon un peu tordu.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Un poil gris reste dans le capuchon.",
        f"{M}|Tu as vu le poil ?",
        f"{E}|Le chat a joué au ballon.",
        f"{P}|Le ballon sèche, un peu plat, près des chaussures.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai boutonné, sans courir.",
        f"{N}|Derrière la vitre, le ballon n'est plus sous le banc.",
        f"{N}|Le clic du crochet tient, avec les boutons.",
    ), "chat,capuchon", "crochet,boutons", "grain de terre grise")

    add(2, 1, 2, L(
        f"{N}|Un chien brun court après le ballon.",
        f"{N}|Il pose une patte sur le manteau bleu, ouvert.",
        f"{E}|Ma patte, pas la tienne.",
        f"{N}|Sarah veut tirer le bleu. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle parle bas. Le chien lève la patte.",
        f"{P}|Il t'a entendu ?",
        f"{E}|Oui. J'ai attendu.",
        f"{N}|Sous un bouton, le grain de terre grise était caché.",
        f"{N}|Sarah boutonne, un par un, le grain dans la main.",
        f"{M}|Le crochet, après les boutons.",
        f"{N}|Elle rentre. Le bleu retrouve le bois, d'un clic.",
        f"{N}|Le grain revient au crochet, sorti du bouton.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, une patte de boue au dos.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Le troisième bouton brille, un peu plus lâche.",
        f"{M}|Tu as vu le bouton ?",
        f"{E}|Le chien a marché dessus.",
        f"{P}|Le ballon a une trace de patte, ronde.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai parlé, puis j'ai boutonné.",
        f"{N}|Derrière la vitre, plus de patte sur le tissu.",
        f"{N}|Le clic du crochet tient, boutonné.",
    ), "chien,bouton", "crochet,boutons", "grain de terre grise")

    add(2, 1, 3, L(
        f"{N}|Une poule picore le ballon, puis un bouton bleu.",
        f"{N}|Le grain de terre grise est collé au bouton.",
        f"{E}|C'est un bouton, poule.",
        f"{N}|Sarah veut chasser le bec. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe, écoute le gravier.",
        f"{M}|Elle va le détacher, tu crois ?",
        f"{E}|Peut-être. Je la laisse.",
        f"{N}|La poule lâche. Sarah décroche le grain du bouton.",
        f"{N}|Elle boutonne. Le bleu est fermé, enfin.",
        f"{P}|Le crochet, maintenant.",
        f"{N}|Elle rentre. Le clic, net, sur le bois.",
        f"{N}|Le grain retrouve le crochet, sorti du bouton.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, un bouton un peu luisant.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume reste accrochée au troisième bouton.",
        f"{M}|Tu as vu la plume ?",
        f"{E}|La poule a picoré le bouton.",
        f"{P}|Le ballon a un trou de bec, minuscule.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai laissé le bec, puis j'ai pris.",
        f"{N}|Derrière la vitre, la poule picore une vraie graine.",
        f"{N}|Le clic du crochet tient, luisant.",
    ), "poule,bouton", "crochet,boutons", "grain de terre grise")

    add(2, 2, 1, L(
        f"{N}|Un chat gris marche sur le bord du seau.",
        f"{N}|Le seau bascule sur le manteau bleu.",
        f"{E}|Mes boutons !",
        f"{N}|Sarah veut soulever le seau d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le bord, écoute le métal.",
        f"{P}|Il va sauter, tu crois ?",
        f"{E}|S'il a les pattes mouillées. Je reste.",
        f"{N}|Le chat saute. Dans une boutonnière, le grain de terre grise tient.",
        f"{N}|Sarah sort le grain, boutonne, reprend le bleu.",
        f"{M}|Le crochet n'a pas d'eau.",
        f"{N}|Elle rentre. Le clic, sur le bois sec.",
        f"{N}|Le grain revient au crochet, sorti du bouton.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, une auréole d'eau au bas.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Un poil gris reste collé à une boutonnière.",
        f"{M}|Tu as vu le poil ?",
        f"{E}|Le chat a marché sur le seau.",
        f"{P}|Le seau bleu sèche, renversé, près du paillasson.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai attendu le saut.",
        f"{N}|Derrière la vitre, le seau ne penche plus.",
        f"{N}|Le clic du crochet tient, sec.",
    ), "chat,seau", "crochet,eau", "grain de terre grise")

    add(2, 2, 2, L(
        f"{N}|Un chien brun met le nez dans le seau.",
        f"{N}|L'anse accroche un bouton, plus fort.",
        f"{E}|Lâche le bouton.",
        f"{N}|Sarah veut tirer. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle décroche l'anse, lentement, bouton par bouton.",
        f"{P}|Le fil a tenu, tu vois ?",
        f"{E}|Il a tenu. J'ai été lente.",
        f"{N}|Sur l'anse, le grain de terre grise est collé.",
        f"{N}|Sarah le prend. Le bleu se ferme, un par un.",
        f"{M}|Le crochet, après l'anse.",
        f"{N}|Elle rentre. Le clic, net, sans fil tendu.",
        f"{N}|Le grain, de l'anse, revient au bois.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, un bouton un peu tiré.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|L'anse du seau a une odeur de chien.",
        f"{M}|Tu as vu le bouton ?",
        f"{E}|Le nez a tiré l'anse.",
        f"{P}|Le seau bleu a le bord humide, près des chaussures.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai décroché, lentement.",
        f"{N}|Derrière la vitre, plus d'anse dans le tissu.",
        f"{N}|Le clic du crochet tient, sans tension.",
    ), "chien,anse", "crochet,seau", "grain de terre grise")

    add(2, 2, 3, L(
        f"{N}|Une poule entre dans le seau, trop à l'aise.",
        f"{N}|Elle picore l'eau. Le grain de terre grise tourne.",
        f"{E}|Sors, poule.",
        f"{N}|Sarah veut soulever le seau. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le bord, écoute l'eau.",
        f"{M}|Elle va sauter, tu crois ?",
        f"{E}|Si je reste calme. Je reste.",
        f"{N}|La poule saute. Le grain reste sur le bord.",
        f"{N}|Sarah le prend, boutonne le bleu, rentre.",
        f"{P}|Le crochet n'a pas d'eau.",
        f"{N}|Le clic, sec, sur le bois.",
        f"{N}|Le grain, du bord, revient au crochet.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, une éclaboussure au bas.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume flotte dans le seau, au seuil.",
        f"{M}|Tu as vu la plume ?",
        f"{E}|La poule a pris le seau.",
        f"{P}|Le seau bleu a le bord luisant, vide.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai attendu le saut, sans crier.",
        f"{N}|Derrière la vitre, plus de poule dans le bleu.",
        f"{N}|Le clic du crochet tient, luisant.",
    ), "poule,seau", "crochet,eau", "grain de terre grise")

    add(2, 3, 1, L(
        f"{N}|Un chat gris emporte le doudou hors du capuchon bleu.",
        f"{N}|Le manteau reste sur le banc, ouvert.",
        f"{E}|Rends l'ami.",
        f"{N}|Sarah veut le rattraper. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle observe le capuchon, écoute le jardin.",
        f"{P}|Le bleu, d'abord, tu crois ?",
        f"{E}|Le bleu. Le doudou reviendra.",
        f"{N}|Dans le capuchon, le grain de terre grise est resté.",
        f"{N}|Sarah reprend le bleu, le grain, boutonne.",
        f"{M}|Le crochet, pour le bleu.",
        f"{N}|Le chat laisse le doudou près de la chaise, plus tard.",
        f"{N}|Le clic du crochet, net, dans l'entrée.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, le capuchon vide.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Le doudou, sur la chaise, a un poil gris.",
        f"{M}|Tu as vu le capuchon ?",
        f"{E}|Le chat a pris l'ami. Pas le bleu.",
        f"{P}|Le doudou sèche, loin du capuchon.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai choisi le bleu, d'abord.",
        f"{N}|Derrière la vitre, le banc n'a plus de capuchon.",
        f"{N}|Le clic du crochet tient, vide au col.",
    ), "chat,capuchon", "crochet,chaise", "grain de terre grise")

    add(2, 3, 2, L(
        f"{N}|Un chien brun secoue le doudou. Les boutons bleus s'ouvrent.",
        f"{N}|Le manteau glisse. La terre le tache.",
        f"{E}|Doucement, toi.",
        f"{N}|Sarah veut saisir le doudou. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle attend la fin de la secousse.",
        f"{P}|Les boutons, après, un par un ?",
        f"{E}|Un par un. Sous le troisième, le grain.",
        f"{N}|Sous le troisième bouton, le grain de terre grise tient.",
        f"{N}|Sarah boutonne. Le bleu se ferme, enfin.",
        f"{M}|Le crochet, après la terre.",
        f"{N}|Elle secoue un peu, dehors, puis rentre.",
        f"{N}|Le clic, et le grain au bois.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, une tache de terre au bas.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Le troisième bouton est le plus sage.",
        f"{M}|Tu as vu le troisième ?",
        f"{E}|Le grain était dessous.",
        f"{P}|Le doudou a les poils en bataille, sur la chaise.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai attendu la secousse.",
        f"{N}|Derrière la vitre, plus de boutons dans l'herbe.",
        f"{N}|Le clic du crochet tient, boutonné.",
    ), "chien,boutons", "crochet,terre", "grain de terre grise")

    add(2, 3, 3, L(
        f"{N}|Une poule picore le doudou, dans le capuchon bleu.",
        f"{N}|Le grain de terre grise tombe du capuchon, sur le chemin.",
        f"{E}|Il s'en va.",
        f"{N}|Sarah veut tout ramasser d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle suit le grain, pas la poule.",
        f"{M}|Le chemin mène où, là ?",
        f"{E}|Vers le crochet. Je le vois.",
        f"{N}|Le grain roule jusqu'à la marche.",
        f"{N}|Sarah reprend le bleu, le doudou à part.",
        f"{P}|Le crochet, pour le bleu.",
        f"{N}|Elle raccroche. Le grain, de la marche, revient au bois.",
        f"{N}|La poule picore ailleurs, sans le capuchon.",
    ), L(
        f"{N}|Dans l'entrée, le bleu pend, le capuchon un peu marqué.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume reste sur la marche, sous le bois.",
        f"{M}|Tu as vu la marche ?",
        f"{E}|Le grain a montré le chemin.",
        f"{P}|Le doudou sèche sur la chaise, sans plume.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai suivi le grain, pas le bec.",
        f"{N}|Derrière la vitre, le capuchon n'est plus un nid.",
        f"{N}|Le clic du crochet tient, guidé.",
    ), "poule,chemin", "crochet,marche", "grain de terre grise")

    add(3, 1, 1, L(
        f"{N}|Un chat gris se cache sous l'ourlet vert, trop long.",
        f"{N}|Sarah veut tirer l'ourlet. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle soulève le bas, comme un rideau, lentement.",
        f"{E}|C'est toi, là-dessous.",
        f"{N}|Le chat sort. Sur l'ourlet, le grain de terre grise tient.",
        f"{P}|Tu l'as levé, sans tirer ?",
        f"{E}|Sans tirer. Il est trop long, c'est tout.",
        f"{N}|Sarah ramasse le grain, soulève l'ourlet pour marcher.",
        f"{M}|Le crochet, lui, n'a pas d'ourlet par terre.",
        f"{N}|Elle rentre. Le vert retrouve le bois, d'un clic.",
        f"{N}|L'ourlet ne traîne plus. Le grain est au crochet.",
        f"{N}|Le ballon reste contre la pierre, sage.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, l'ourlet un peu terreux.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Un poil gris reste au bas, caché.",
        f"{M}|Tu as vu l'ourlet ?",
        f"{E}|Le chat était dessous.",
        f"{P}|Le ballon sèche contre le paillasson, un peu plat.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai levé, sans tirer.",
        f"{N}|Derrière la vitre, plus de chat sous le vert.",
        f"{N}|Le clic du crochet tient, l'ourlet en l'air.",
    ), "chat,ourlet", "crochet,ourlet", "grain de terre grise")

    add(3, 1, 2, L(
        f"{N}|Un chien brun marche sur l'ourlet vert. Sarah est coincée.",
        f"{N}|Elle veut tirer. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle parle. Le chien lève la patte.",
        f"{E}|Merci, toi. J'ai ma jambe.",
        f"{N}|Sur l'ourlet, le grain de terre grise a un frère de boue.",
        f"{P}|Tu soulèves, maintenant ?",
        f"{E}|Je soulève. Je ne tire pas.",
        f"{N}|Sarah marche, l'ourlet dans la main, le grain aussi.",
        f"{M}|Le crochet n'écrase rien.",
        f"{N}|Elle rentre. Le vert retrouve le bois, d'un clic.",
        f"{N}|Les deux grains : un au crochet, l'autre brossé dehors.",
        f"{N}|Le ballon, contre la pierre, n'a plus de course.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, une patte de boue à l'ourlet.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|L'autre terre, brossée, reste sur la marche.",
        f"{M}|Tu as vu les deux ?",
        f"{E}|Un vrai, un de patte. J'ai gardé le vrai.",
        f"{P}|Le ballon a une trace de patte, au côté.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai parlé, puis j'ai levé.",
        f"{N}|Derrière la vitre, plus de jambe coincée.",
        f"{N}|Le clic du crochet tient, l'ourlet libre.",
    ), "chien,ourlet", "crochet,marche", "grain de terre grise")

    add(3, 1, 3, L(
        f"{N}|Une poule picore l'ourlet vert, tout le bas.",
        f"{N}|Le grain de terre grise l'intéresse, au bord.",
        f"{E}|C'est pas une graine, poule.",
        f"{N}|Sarah veut reculer d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle s'accroupit, observe le bec.",
        f"{M}|Elle va le laisser, tu crois ?",
        f"{E}|Si je ne bouge pas trop.",
        f"{N}|La poule laisse le grain. Sarah le prend, soulève l'ourlet.",
        f"{P}|Le crochet, sans traîner.",
        f"{N}|Elle rentre. Le vert ne frotte plus les feuilles.",
        f"{N}|Le clic, et le grain au bois.",
        f"{N}|Le ballon, contre la pierre, n'a plus de course.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, l'ourlet un peu picoré.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume reste collée au bas, comme un timbre.",
        f"{M}|Tu as vu la plume ?",
        f"{E}|La poule a cru au bas.",
        f"{P}|Le ballon a une trace de terre, au bas aussi.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|Je me suis baissée, sans reculer.",
        f"{N}|Derrière la vitre, l'ourlet ne mange plus le jardin.",
        f"{N}|Le clic du crochet tient, le bas en l'air.",
    ), "poule,ourlet", "crochet,plume", "grain de terre grise")

    add(3, 2, 1, L(
        f"{N}|Un chat gris s'installe dans le seau. L'ourlet vert l'entoure.",
        f"{N}|Sarah veut tout dégager d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle détorille l'ourlet, lentement, autour de l'anse.",
        f"{E}|Toi le seau. Moi le vert.",
        f"{N}|Le chat saute. Au fond du seau, le grain de terre grise brille.",
        f"{P}|Chacun sa place, là ?",
        f"{E}|Oui. L'ourlet, plus autour.",
        f"{N}|Sarah prend le grain, soulève le vert, rentre.",
        f"{M}|Le crochet n'a pas d'anse.",
        f"{N}|Le clic, net. L'ourlet ne touche plus le seau.",
        f"{N}|Le grain, du fond, revient au bois.",
        f"{N}|Le seau, vide, reste au jardin.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, l'ourlet libre, sans anse.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Un poil gris reste au fond du seau, au seuil.",
        f"{M}|Tu as vu le fond ?",
        f"{E}|Le chat y était. Le grain aussi.",
        f"{P}|Le seau bleu sèche, vide, près du paillasson.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai détortillé, sans tout tirer.",
        f"{N}|Derrière la vitre, plus d'ourlet autour du seau.",
        f"{N}|Le clic du crochet tient, dénoué.",
    ), "chat,anse", "crochet,seau", "grain de terre grise")

    add(3, 2, 2, L(
        f"{N}|Un chien brun prend l'anse et l'ourlet, ensemble.",
        f"{N}|Sarah veut courir après. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle s'immobilise. Le chien s'arrête aussi.",
        f"{E}|Pose. Les deux.",
        f"{N}|Il pose. Sur l'anse, le grain de terre grise est collé.",
        f"{P}|Il t'a vue, arrêtée ?",
        f"{E}|Oui. Alors il a posé.",
        f"{N}|Sarah sépare l'anse et l'ourlet, le grain dans la main.",
        f"{M}|Le crochet, pour le vert seulement.",
        f"{N}|Elle rentre. Le clic, sans anse.",
        f"{N}|Le grain, de l'anse, revient au bois.",
        f"{N}|Le seau reste au jardin, l'anse libre.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, l'ourlet sans nœud.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|L'anse du seau a une marque de dents, petite.",
        f"{M}|Tu as vu l'anse ?",
        f"{E}|Le chien a pris les deux. J'ai séparé.",
        f"{P}|Le seau bleu a l'anse un peu tordue, au seuil.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|Je me suis arrêtée. Lui aussi.",
        f"{N}|Derrière la vitre, plus d'ourlet dans l'anse.",
        f"{N}|Le clic du crochet tient, séparé.",
    ), "chien,anse", "crochet,seau", "grain de terre grise")

    add(3, 2, 3, L(
        f"{N}|Une poule picore sous l'ourlet, près du seau.",
        f"{N}|Le vert trop long cache sa graine, pour de faux.",
        f"{E}|Je te vois, poule.",
        f"{N}|Sarah veut soulever d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle lève l'ourlet, lentement, comme un rideau.",
        f"{M}|Le grain, il est où ?",
        f"{E}|Sous l'ourlet. Je le vois.",
        f"{N}|Sous le bas, le grain de terre grise tient, à l'abri.",
        f"{N}|Sarah le prend, soulève le vert, rentre.",
        f"{P}|Le crochet n'est pas un abri de poule.",
        f"{N}|Le clic. Le grain, de l'abri, revient au bois.",
        f"{N}|Le seau, lui, n'a plus de toit de tissu.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, l'ourlet un peu relevé.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume reste sous le seau, au seuil.",
        f"{M}|Tu as vu l'abri ?",
        f"{E}|C'était l'ourlet. Plus maintenant.",
        f"{P}|Le seau bleu sèche, sans toit, près des chaussures.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai levé le rideau, lentement.",
        f"{N}|Derrière la vitre, la poule picore à découvert.",
        f"{N}|Le clic du crochet tient, le bas en l'air.",
    ), "poule,ourlet", "crochet,seau", "grain de terre grise")

    add(3, 3, 1, L(
        f"{N}|Un chat gris s'endort sur le doudou, sous le vert trop long.",
        f"{N}|Sarah veut tout soulever d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle lève le vert, comme un rideau, lentement.",
        f"{E}|C'est toi, sur l'ami.",
        f"{N}|Le chat ouvre un œil, puis part.",
        f"{N}|Sur la doublure, le grain de terre grise tient.",
        f"{P}|Tu as levé le rideau, c'est ça ?",
        f"{E}|Le rideau. Pas d'un coup.",
        f"{N}|Sarah prend le grain, le doudou à part, le vert sur le bras.",
        f"{M}|Le crochet n'est pas un lit.",
        f"{N}|Elle rentre. Le clic, et le grain au bois.",
        f"{N}|Le doudou va sur la chaise, sans chat.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, la doublure un peu chaude.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Un poil gris reste sur le doudou, sur la chaise.",
        f"{M}|Tu as vu le poil ?",
        f"{E}|Le chat a dormi dessous.",
        f"{P}|Le doudou sèche, loin du capuchon.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai levé le rideau, lentement.",
        f"{N}|Derrière la vitre, plus de nid sous le vert.",
        f"{N}|Le clic du crochet tient, la doublure au repos.",
    ), "chat,doudou", "crochet,tissu", "grain de terre grise")

    add(3, 3, 2, L(
        f"{N}|Un chien brun s'allonge sur le vert et le doudou.",
        f"{N}|Sarah veut tirer le tissu. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle s'assoit, attend, écoute le jardin.",
        f"{E}|Quand tu veux, tu te lèves.",
        f"{N}|Le chien se lève. Près de la botte, le grain de terre grise brille.",
        f"{P}|Il était sur ta place, c'est ça ?",
        f"{E}|Sur le vert. J'ai attendu.",
        f"{N}|Sarah ramasse le grain, près de la botte d'automne.",
        f"{N}|Elle reprend le vert, le doudou à part.",
        f"{M}|Le crochet, pour le vert.",
        f"{N}|Elle rentre. Le clic, et le grain au bois.",
        f"{N}|Le doudou, lui, n'est plus un tapis de chien.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, un peu chaud du chien.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Près de la botte, l'herbe a une trace allongée.",
        f"{M}|Tu as vu la botte ?",
        f"{E}|Le grain était à côté. J'ai attendu.",
        f"{P}|Le doudou sèche sur la chaise, plus plat.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|Je me suis assise, sans tirer.",
        f"{N}|Derrière la vitre, plus de tapis de chien.",
        f"{N}|Le clic du crochet tient, tiède un moment.",
    ), "chien,doudou", "crochet,bottes", "grain de terre grise")

    add(3, 3, 3, L(
        f"{N}|Une poule se glisse sous le capuchon, avec le doudou.",
        f"{N}|Sarah veut ouvrir d'un coup. Elle s'arrête.",
        f"{N}|Cette fois, elle refuse de foncer.",
        f"{N}|Elle ouvre le capuchon, lentement, comme une porte.",
        f"{E}|Toi ici, poule. Toi là, ami.",
        f"{N}|La poule sort. Dans le capuchon, le grain de terre grise brille.",
        f"{M}|Il s'était caché, le grain ?",
        f"{E}|Avec eux. Je l'ai vu, après.",
        f"{N}|Sarah prend le grain, le vert, le doudou à part.",
        f"{P}|Le crochet, pour le vert seulement.",
        f"{N}|Elle rentre. Le clic, et le grain au bois.",
        f"{N}|Le capuchon, vide, n'est plus un abri.",
        f"{N}|La poule picore le gravier, dehors.",
    ), L(
        f"{N}|Dans l'entrée, le vert pend, le capuchon ouvert, vide.",
        f"{N}|Le grain de terre grise est revenu sur le crochet.",
        f"{N}|Une plume reste dans le capuchon, comme un secret.",
        f"{M}|Tu as vu le secret ?",
        f"{E}|La poule et l'ami. Le grain, avec eux.",
        f"{P}|Le doudou sèche sur la chaise, sans plume.",
        f"{N}|La botte d'automne a sa trace ronde.",
        f"{E}|J'ai ouvert, comme une porte.",
        f"{N}|Derrière la vitre, le capuchon n'abrite plus.",
        f"{N}|Le clic du crochet tient, le capuchon au repos.",
    ), "poule,capuchon", "crochet,capuchon", "grain de terre grise")

    return d


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> None:
        out[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "botte,crochet", {"emphasis": "grain de terre grise"})
    put(
        "CHK_T0001_P0000",
        L(
            f"{N}|Trois manteaux attendent sur le crochet.",
            f"{M}|Le rouge, le bleu, ou le vert ?",
        ),
        "choice",
        "",
        {"fields": {
            "option_1_label": "rouge",
            "option_2_label": "bleu",
            "option_3_label": "vert",
        }},
    )

    for a, t1 in T1.items():
        put(f"CHK_T0001_P000{a}", t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        put(
            f"CHK_T0001_P000{a}_Q0001",
            t1["question"],
            "clue",
            "",
            {"night_policy": "skip", "fields": Q_FIELDS, "emphasis": "manteau"},
        )
        put(f"CHK_T0001_P000{a}_C0001", t1["confirm"], "confirm", "crochet,porte", {"emphasis": "crochet"})
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

    t2 = t2_scenes_fixed()
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            lines, sons, emp = t2[(a, b)]
            cid = f"CHK_T0001_P000{a}_T0002_P000{b}"
            put(cid, lines, "obstacle", sons, {"emphasis": emp})
            adult = P if (a + b) % 2 == 0 else M
            put(
                f"{cid}_T0003_P0000",
                L(
                    f"{N}|{T3Q[(a, b)]}",
                    f"{adult}|Le chat, le chien, ou la poule ?",
                ),
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le chat",
                    "option_2_label": "le chien",
                    "option_3_label": "la poule",
                }},
            )

    scenes = t3_end()
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                passage, ending, s3, se, emp = scenes[(a, b, c)]
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(base, passage, "resolution", s3, {"emphasis": emp})
                put(f"{base}_F0001", ending, "ending", se, {"emphasis": "crochet"})

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
        "Papa range les chaussures d'été. Un grain de terre grise saute "
        "d'une botte et se pose sur le crochet bas. Sarah veut les feuilles "
        "du banc aux feuilles avant le vent. Elle court trop vite : le "
        "manteau résiste, reste, ou glisse. Le sourire disparaît. Rouge, "
        "bleu ou vert part avec elle. Ballon, seau ou doudou rusent plus "
        "fort. Chat, chien ou poule touchent le tissu. Elle refuse de "
        "foncer, retrouve le grain, accroche. Le clic paie le début."
    )
    merged["title"] = TITLE
    merged["characters"] = "Sarah, papa, maman"
    merged["setting"] = "entrée, crochet, jardin gris d'automne"
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
    opening_low = out["CHK_T0000_P0000"]["text"].lower()
    if "grain de terre grise" not in opening_low:
        raise SystemExit("indice absent de l'ouverture")
    if "en ce moment" not in opening_low:
        raise SystemExit("en ce moment absent")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    relecture(
        SID,
        TITLE,
        (
            "- **Public :** N2 (3–6 ans), audio familial\n"
            "- **Leçon :** AUT.AFF.002 — accrocher / poser le manteau à sa "
            "place, vécue (le clic du crochet, le grain revenu), jamais dite\n"
            "- **Personnages :** Sarah, papa, maman\n"
            "- **Objet :** manteau rouge, bleu ou vert (il part avec elle)\n"
            "- **Lieu nommé :** banc aux feuilles, crochet bas, entrée au bois mouillé\n"
            "- **Mission :** aller au banc aux feuilles avant le vent, "
            "rapporter une feuille, raccrocher\n"
            "- **Déclencheur :** le manteau résiste, reste, ou révèle le grain\n"
            "- **1er imprévu :** manche à l'envers / boutons / ourlet trop long\n"
            "- **2e ruse :** ballon (manche, boutons, ourlet), seau (poche, "
            "anse, nœud), doudou (banc, flaque, capuchon)\n"
            "- **Indice du début :** grain de terre grise ; la fin le ramène au crochet"
        ),
        (
            "Reprise F-NAR-019 P2. Noyau « Le manteau du jardin gris » "
            "conservé (entrée, crochet, jardin gris d'automne). "
            "Ouverture inventée (chaussures d'été, botte, grain). "
            "T1 ne retire pas l'équipement : le manteau part avec Sarah. "
            "Impatience, petit découragement, fierté calme. "
            "Adulte guide peu, pas de règle dite. Plus de tout doux / encore / "
            "déjà / tout calme. Un merci vécu (mains au chaud). Question "
            "adulte. 27 fins, 27 T3, 9 T2 textuellement distincts. "
            "Monde ≠ TREE-AUT-032 / 037 / 047. "
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

