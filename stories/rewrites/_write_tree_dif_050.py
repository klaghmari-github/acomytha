#!/usr/bin/env python3
"""TREE-DIF-050 — Les deux cerceaux d'Aniss, jusqu'à la porte jaune (F-NAR-019, N2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-050"
N2 = LIMITS["N2"]
TITLE = "Les deux cerceaux d'Aniss, jusqu'à la porte jaune"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "marque fine",
    "ombre-flèche",
    "ombre en forme de flèche",
    "ancre minuscule",
    "étoile brune",
    "fil pâle",
    "croissant d'eau",
    "virgule farine",
    "bouton nacre",
    "nœud raphia",
    "pois ivoire",
    "grain savon",
    "grain vanille",
    "pastille colle",
    "virgule buée",
    "capuchon penche",
    "grain doré",
    "brin safran",
    "anneau liège",
    "clou tête ronde",
    "grain d'ambre",
    "goutte de cire",
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
    "groseille",
    "statue",
    "galet",
    "poisson",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de brique",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=deux_rythmes_dès_le_seuil; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note=(
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton_choix_change_la_manière; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="cerceau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=où_voyage_l_objet; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="cerceau",
        note=(
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=les_trois_affaires_partent; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=élan; intensite=2; "
            "destinataire=enfant; sous_texte=la_premiere_poussée_rate; "
            "tempo=vif; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=Mila_a_son_rythme; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de brique",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=il_refuse_de_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de brique",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_grain_a_trouvé_son_trou; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

T1_META = {
    1: dict(lab="le grand cerceau", short="grand", sons="cerceau,bois"),
    2: dict(lab="le petit cerceau", short="petit", sons="cerceau,herbe"),
    3: dict(lab="le bâton", short="bâton", sons="baton,bois"),
}
T2_META = {
    1: dict(lab="le chemin de terre", short="terre", sons="terre,poussiere"),
    2: dict(lab="l'herbe du tilleul", short="herbe", sons="herbe,feuilles"),
    3: dict(lab="le perron", short="perron", sons="pas,bois"),
}
T3_LABS = {
    1: ("les mains de Mila", "le pont du grand", "rouler à deux"),
    2: ("le couloir de Mila", "les mains d'Aniss", "écarter ensemble"),
    3: ("Aniss porte", "Mila reçoit", "la dernière marche"),
}
T3_SONS = {
    1: {1: "mains,bois", 2: "cerceau,terre", 3: "cerceaux,poussiere"},
    2: {1: "herbe,pas", 2: "mains,racine", 3: "tiges,herbe"},
    3: {1: "pas,bois", 2: "cerceau,pas", 3: "marche,brique"},
}

Q_FIELDS = {
    1: {
        "expected_answer": "hanche",
        "accepted_examples": "hanche | la hanche | contre la hanche | sa hanche",
        "retry_prompt": "Le grand cerceau est contre la hanche.",
    },
    2: {
        "expected_answer": "main",
        "accepted_examples": "main | la main | dans la main | sa main",
        "retry_prompt": "Le petit cerceau est dans la main.",
    },
    3: {
        "expected_answer": "bras",
        "accepted_examples": "bras | le bras | sous le bras | son bras",
        "retry_prompt": "Le bâton est sous le bras.",
    },
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
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
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
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
    out["pitch_ssml"] = m["pitchSsml"]
    out["pitch_xai_tag"] = m["pitchTag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before_ms", 0)
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
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    out.update(extra.get("fields") or {})
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms", "night_policy", "fields"):
            continue
        out[k] = v
    return out


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


# Ouverture : deux rythmes face à la porte. Indice unique = grain de brique.
OPENING = [
    "narrateur|Mila saute sur un pied, face à la porte.",
    "narrateur|Aniss tient le cerceau orange, les mains prêtes.",
    "narrateur|Un grain de brique s'est coincé dans le bois.",
    "narrateur|Le seuil a un trou, de la même taille.",
    "narrateur|La poussière sent le soleil, chaud sur les orteils.",
    "narrateur|Aniss vit ici, avec papa et maman.",
    "narrateur|Le petit bleu dort dans l'herbe.",
    "narrateur|Un bâton de bois attend, près du mur.",
    "narrateur|La peinture jaune tient un peu de poussière.",
    "maman|Tu as vu le grain, Aniss ?",
    "enfant-m|Les deux, jusqu'à la porte jaune !",
    "narrateur|En ce moment, Aniss pousse trop vite.",
    "narrateur|Le grand cerceau part, le petit reste.",
    "narrateur|Mila ne dit rien.",
    "narrateur|Son silence tient, comme une réponse.",
    "narrateur|Le sourire d'Aniss disparaît.",
    "papa|Tu vas sans elle, ou avec elle ?",
    "enfant-m|Avec elle, les deux cerceaux.",
    "maman|Merci, tu l'as attendue.",
    "narrateur|Papa s'accroupit, à leur hauteur.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près du mur.",
    "narrateur|Le grand cerceau, le petit, et le bâton.",
    "maman|Tu prends quoi d'abord, Aniss ?",
]

T1 = {
    1: [
        "narrateur|Aniss saisit le grand cerceau, trop vite.",
        "enfant-m|Je le roule, moi, jusqu'à la porte !",
        "narrateur|Le grain de brique fait tanguer le cercle.",
        "narrateur|Le cerceau tombe, plat, dans la poussière.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Le sourire d'Aniss disparaît.",
        "papa|Garde-le contre ta hanche, droit.",
        "narrateur|Papa s'accroupit, près du bois orange.",
        "narrateur|Aniss cale le grand contre sa hanche.",
        "maman|Le petit, ensuite, pour Mila.",
        "narrateur|Mila serre le petit bleu, sans un mot.",
        "papa|Le bâton, aussi, avec vous.",
        "narrateur|Les trois affaires partent ensemble.",
    ],
    2: [
        "narrateur|Aniss saisit le petit cerceau, trop vite.",
        "enfant-m|Mila, prends-le, on y va !",
        "narrateur|Il le fait rouler vers ses pieds.",
        "narrateur|Mila ne tend pas les mains.",
        "narrateur|Le bleu s'arrête, seul, dans l'herbe.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Le sourire d'Aniss disparaît.",
        "maman|Pose-le dans sa main, sans le lancer.",
        "narrateur|Maman s'accroupit, à leur hauteur.",
        "narrateur|Mila prend le petit, dans sa main.",
        "papa|Le grand, ensuite, à ta hanche.",
        "narrateur|Aniss cale l'orange, puis le bâton.",
        "narrateur|Les trois affaires partent ensemble.",
    ],
    3: [
        "narrateur|Aniss saisit le bâton, trop vite.",
        "enfant-m|Je pousse les deux, d'un coup !",
        "narrateur|Le bâton tape le grand, puis le petit.",
        "narrateur|Les cerceaux s'emmêlent, et tombent.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Le sourire d'Aniss disparaît.",
        "papa|Glisse-le sous ton bras, d'abord.",
        "narrateur|Papa s'accroupit, près du bois.",
        "narrateur|Aniss glisse le bâton sous son bras.",
        "maman|Le grand à la hanche, le petit à Mila.",
        "narrateur|Mila prend le bleu, sans un mot.",
        "enfant-m|J'ai le bâton, sous le bras.",
        "narrateur|Les trois affaires partent ensemble.",
    ],
}

T1_Q = {
    1: [
        "narrateur|Aniss a mis le grand cerceau contre la hanche.",
        "maman|Il est où, ce bois-là ?",
    ],
    2: [
        "narrateur|Mila tient le petit cerceau.",
        "papa|Il est où, ce bleu-là ?",
    ],
    3: [
        "narrateur|Aniss a glissé le bâton.",
        "maman|Il est où, ce bois-là ?",
    ],
}

T1_C = {
    1: [
        "narrateur|La hanche porte le grand cerceau, orange.",
        "enfant-f|Il me monte trop, moi.",
        "enfant-m|Moi, il me va.",
        "maman|Mila est plus petite, c'est tout.",
        "papa|On avance vers la porte ?",
        "enfant-m|Oui, papa.",
        "narrateur|Le grain de brique reste coincé, visible.",
        "narrateur|Un bâton voyage contre le grand.",
    ],
    2: [
        "narrateur|La main de Mila porte le petit bleu.",
        "enfant-f|Celui-là, c'est le mien.",
        "enfant-m|Le grand, c'est le mien.",
        "papa|Deux tailles, deux mains.",
        "maman|On avance vers la porte ?",
        "enfant-m|Oui, maman.",
        "narrateur|Le grain de brique reste coincé, visible.",
        "narrateur|Un bâton voyage contre le grand.",
    ],
    3: [
        "narrateur|Le bras d'Aniss porte le bâton, chaud.",
        "enfant-m|Il va pousser, sans frapper.",
        "enfant-f|Pas trop fort, Aniss.",
        "maman|Le bâton guide, il ne chasse pas.",
        "papa|On avance vers la porte ?",
        "enfant-m|Oui, papa.",
        "narrateur|Le grain de brique reste coincé, visible.",
        "narrateur|Les deux cerceaux voyagent avec eux.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Le chemin se partage, vers la porte.",
        "papa|Le chemin de terre, l'herbe du tilleul, ou le perron ?",
        "maman|Les deux cerceaux viennent avec vous.",
    ],
    2: [
        "narrateur|La porte jaune attend, au bout.",
        "maman|Le chemin de terre, l'herbe du tilleul, ou le perron ?",
        "papa|Le petit bleu reste dans sa main.",
    ],
    3: [
        "narrateur|Le bâton peut choisir la piste.",
        "papa|Le chemin de terre, l'herbe du tilleul, ou le perron ?",
        "maman|On part avec les deux cerceaux.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    carry = {
        1: "le grand à la hanche",
        2: "le petit dans sa main",
        3: "le bâton sous le bras",
    }[a]
    table = {
        (1, 1): [
            f"narrateur|Aniss part sur le chemin de terre, {carry}.",
            "narrateur|La poussière pique le nez, chaude.",
            "enfant-m|Mila, on roule, vite !",
            "narrateur|Mila pose un pied, puis l'autre.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Le grand cerceau part trop fort.",
            "narrateur|Une ornière l'avale, d'un coup.",
            "enfant-m|Il est tombé.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Une pente, plus loin, tirerait le bois sans elle.",
            "maman|Tu fonces, ou tu regardes avec elle ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (1, 2): [
            f"narrateur|Aniss entre dans l'herbe du tilleul, {carry}.",
            "narrateur|Les tiges frottent les chevilles, sèches.",
            "enfant-m|On coupe droit, Mila !",
            "narrateur|Mila saute d'une touffe à l'autre.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Une racine accroche le grand cerceau.",
            "narrateur|Le cercle s'immobilise, de travers.",
            "enfant-m|Il est coincé.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Un couloir d'herbe s'ouvre, trop étroit pour elle.",
            "papa|Tu forces, ou tu regardes avec elle ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (1, 3): [
            f"narrateur|Aniss arrive au perron, {carry}.",
            "narrateur|La première marche lui arrive au genou.",
            "enfant-m|Je monte les deux, Mila !",
            "narrateur|Mila pose un pied, trop bas.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Le grand cerceau tape la pierre, trop haut.",
            "narrateur|Il retombe vers ses genoux.",
            "enfant-m|La marche refuse.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Il pourrait porter les deux, et finir sans elle.",
            "papa|Tu montes seul, ou tu l'attends ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (2, 1): [
            f"narrateur|Mila avance sur la terre, {carry}.",
            "narrateur|La poussière grimpe à ses genoux.",
            "enfant-m|Pousse le bleu, plus vite !",
            "narrateur|Mila s'arrête au bord de l'ornière.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Aniss a trois pas d'avance, trop loin.",
            "narrateur|Le petit bleu penche, prêt à tomber.",
            "enfant-m|Tu viens ?",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|La pente prendrait le petit, sans ses mains.",
            "maman|Tu l'attends, ou tu pars ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (2, 2): [
            f"narrateur|Mila entre dans l'herbe, {carry}.",
            "narrateur|Les tiges cachent le petit bleu, presque.",
            "enfant-m|Le couloir, tout droit !",
            "narrateur|Mila saute, et le bleu disparaît.",
            "narrateur|Elle ne dit rien.",
            "enfant-m|Où est-il ?",
            "narrateur|Aniss écarte trop vite, trop fort.",
            "narrateur|Une tige claque, et rien.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Le couloir d'herbe l'avalerait, sans elle.",
            "papa|Tu cherches avec elle, ou tu cours ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (2, 3): [
            f"narrateur|Mila arrive au perron, {carry}.",
            "narrateur|Le petit bleu lui monte trop, trop lourd.",
            "enfant-m|Passe-le, je le porte !",
            "narrateur|Mila serre le bois, et s'arrête.",
            "narrateur|Elle ne dit rien.",
            "narrateur|La marche est trop haute, pour ses genoux.",
            "narrateur|Le bleu glisse d'un cran, vers le bas.",
            "enfant-m|Je le prends, moi.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Il pourrait finir les deux, sur le seuil.",
            "maman|Tu prends tout, ou tu lui laisses sa place ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (3, 1): [
            f"narrateur|Aniss guide sur la terre, {carry}.",
            "narrateur|Le bâton trace une ligne, trop droite.",
            "enfant-m|Les deux, d'un coup, Mila !",
            "narrateur|Mila suit la ligne, plus lente.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Le bâton pousse trop, dans l'ornière.",
            "narrateur|Les deux cerceaux se coincent, ensemble.",
            "enfant-m|Ça bloque.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|La pente emporterait le bâton, et le grand.",
            "papa|Tu pousses plus fort, ou tu ralentis ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (3, 2): [
            f"narrateur|Aniss lève une tige, {carry}.",
            "narrateur|L'herbe du tilleul sent le vert tiède.",
            "enfant-m|Je fais le passage, Mila !",
            "narrateur|Mila attend, un pied en l'air.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Le bâton soulève la racine, trop tôt.",
            "narrateur|La racine retombe, avant ses pas.",
            "enfant-m|C'est refermé.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Le couloir d'herbe l'appellerait, sans elle.",
            "maman|Tu ouvres pour toi, ou pour elle ?",
            "enfant-m|Je ne fonce pas.",
        ],
        (3, 3): [
            f"narrateur|Aniss pose le bâton, {carry}.",
            "narrateur|Le bois tape la première marche, sec.",
            "enfant-m|Je le hisse, les deux d'un coup !",
            "narrateur|Mila reste en bas, les mains vides.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Le bâton glisse sur la pierre, trop vite.",
            "narrateur|Le grand cerceau manque le nez d'Aniss.",
            "enfant-m|Presque.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Le bâton pourrait finir le seuil, sans elle.",
            "papa|Tu le forces, ou tu descends la main ?",
            "enfant-m|Je ne fonce pas.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Le cerceau demande une aide, maintenant.",
        "papa|Les mains de Mila, le pont du grand, ou rouler à deux ?",
        "maman|On avance avec elle, pas devant.",
    ],
    2: [
        "narrateur|L'herbe cache un passage, peut-être.",
        "maman|Le couloir de Mila, les mains d'Aniss, ou écarter ensemble ?",
        "papa|Personne ne dit le geste.",
    ],
    3: [
        "narrateur|La marche haute attend, trop sèche.",
        "papa|Aniss porte, Mila reçoit, ou la dernière marche ?",
        "maman|Le seuil garde son trou, pour le grain.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    obj = {
        1: "le grand à la hanche",
        2: "le petit dans sa main",
        3: "le bâton sous le bras",
    }[a]
    arrive = {
        (1, 1): [
            f"narrateur|Aniss tend les mains, {obj}.",
            "enfant-m|Tes mains, Mila, sur le bois.",
            "narrateur|Mila recule les doigts, d'abord.",
        ],
        (1, 2): [
            f"narrateur|Aniss couche le grand, {obj}.",
            "enfant-m|Un pont, au-dessus de l'ornière.",
            "narrateur|Le petit bleu attend, trop bas.",
        ],
        (1, 3): [
            f"narrateur|Aniss se place à côté, {obj}.",
            "enfant-m|On roule, tous les deux.",
            "narrateur|La pente tire le bois, vers la porte.",
        ],
        (2, 1): [
            f"narrateur|Aniss écarte les tiges, {obj}.",
            "enfant-m|Un couloir, large comme toi.",
            "narrateur|Mila mesure l'écart, avec son saut.",
        ],
        (2, 2): [
            f"narrateur|Aniss met ses mains à terre, {obj}.",
            "enfant-m|Je tiens la racine, pour toi.",
            "narrateur|Mila cherche le bleu, dans l'ombre.",
        ],
        (2, 3): [
            f"narrateur|Aniss prend une tige, {obj}.",
            "enfant-m|On écarte, ensemble.",
            "narrateur|Mila ne dit rien, puis tire une tige.",
        ],
        (3, 1): [
            f"narrateur|Aniss soulève son cerceau, {obj}.",
            "enfant-m|Le mien, je le porte.",
            "narrateur|Le bleu reste dans les mains de Mila.",
        ],
        (3, 2): [
            f"narrateur|Aniss tend le bois, {obj}.",
            "enfant-m|Tu le reçois, sur la marche.",
            "narrateur|Mila lève les mains, puis les baisse.",
        ],
        (3, 3): [
            f"narrateur|Aniss pose un pied, {obj}.",
            "enfant-m|La dernière, ensemble.",
            "narrateur|Mila pose le sien, un temps après.",
        ],
    }[(b, c)]
    body = {
        1: [
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "enfant-m|Je cherche, sans foncer.",
        ],
        2: [
            "narrateur|Personne ne dit où courir.",
            "narrateur|Le sourire d'Aniss reste parti.",
            "narrateur|Maman s'accroupit, près de l'herbe.",
            "enfant-m|J'écoute le lieu, d'abord.",
        ],
        3: [
            "narrateur|Personne ne pousse leurs talons.",
            "narrateur|L'envie de finir lui pique les doigts.",
            "narrateur|Papa s'accroupit, sur la marche.",
            "enfant-m|Je regarde le bois, sans forcer.",
        ],
    }[c]
    listen = {
        1: "narrateur|Il écoute la poussière, puis le cerceau.",
        2: "narrateur|Il écoute l'herbe, puis le cerceau.",
        3: "narrateur|Il écoute la pierre, puis le cerceau.",
    }[b]
    pay = "narrateur|Aniss retrouve le grain de brique, coincé."
    gesture = {
        (1, 1): [
            "narrateur|Il pose ses mains derrière les siennes.",
            "narrateur|Ils poussent au rythme de Mila.",
        ],
        (1, 2): [
            "narrateur|Mila pousse le petit bleu sur le grand.",
            "narrateur|L'ornière passe dessous, sans les avaler.",
        ],
        (1, 3): [
            "narrateur|Deux cerceaux, deux vitesses, une même poussière.",
            "narrateur|Aniss ralentit, jusqu'à son saut.",
        ],
        (2, 1): [
            "narrateur|Voilà un couloir, large comme son saut.",
            "narrateur|Mila saute, et le bleu la suit.",
        ],
        (2, 2): [
            "narrateur|Ses mains tiennent la racine, ouvertes.",
            "narrateur|Mila glisse le bleu, entre les doigts.",
        ],
        (2, 3): [
            "narrateur|Deux paires de mains écartent les tiges.",
            "narrateur|Le passage tient, le temps de Mila.",
        ],
        (3, 1): [
            "narrateur|Il porte le sien, marche après marche.",
            "narrateur|Il attend qu'elle pose le pied.",
        ],
        (3, 2): [
            "narrateur|Il tend le bois, sans le lâcher trop tôt.",
            "narrateur|Mila le reçoit, quand elle est prête.",
        ],
        (3, 3): [
            "narrateur|Ils montent la dernière, pas à pas.",
            "narrateur|Deux souffles, sur la même brique.",
        ],
    }[(b, c)]
    traces = {
        (1, 1, 1): "narrateur|Une ligne de brique file, sous leurs mains.",
        (1, 1, 2): "narrateur|Le pont du grand a une virgule rouge.",
        (1, 1, 3): "narrateur|Deux traces inégales, dans la poussière.",
        (1, 2, 1): "narrateur|Le couloir garde un grain, au bord.",
        (1, 2, 2): "narrateur|La racine lâche une poudre rouge.",
        (1, 2, 3): "narrateur|Une tige pliée montre le passage.",
        (1, 3, 1): "narrateur|Le grand orange a un peu de pierre, au bois.",
        (1, 3, 2): "narrateur|Les mains de Mila sentent le grain.",
        (1, 3, 3): "narrateur|La dernière brique a deux empreintes.",
        (2, 1, 1): "narrateur|Une virgule de poussière reste au petit bleu.",
        (2, 1, 2): "narrateur|Sous le pont, le grain de brique brille.",
        (2, 1, 3): "narrateur|Plus lent, le bleu roule, et tient.",
        (2, 2, 1): "narrateur|Voilà le couloir, qui sent le petit bleu.",
        (2, 2, 2): "narrateur|Les mains d'Aniss ont une poudre rouge.",
        (2, 2, 3): "narrateur|Une tige pliée garde le bleu.",
        (2, 3, 1): "narrateur|Mila a reçu le bleu, plus haut.",
        (2, 3, 2): "narrateur|Contre la porte, le petit penche.",
        (2, 3, 3): "narrateur|Deux souffles, sur le seuil de brique.",
        (3, 1, 1): "narrateur|Au bout du bâton, une poussière rouge tient.",
        (3, 1, 2): "narrateur|Sur le pont, le grain de brique a marqué.",
        (3, 1, 3): "narrateur|Entre les deux cerceaux, le bâton s'endort.",
        (3, 2, 1): "narrateur|Pendant le temps de Mila, le bâton a tenu.",
        (3, 2, 2): "narrateur|Une racine a lâché le grain.",
        (3, 2, 3): "narrateur|Voilà le bâton, une tige coincée.",
        (3, 3, 1): "narrateur|Contre le gond, le bâton tape, puis se tait.",
        (3, 3, 2): "narrateur|Mila tient le bâton, plus petit que le gond.",
        (3, 3, 3): "narrateur|Calé sur la marche, un grain tient.",
    }[(a, b, c)]
    almost = {
        (1, 1, 1): "narrateur|Ses mains, seules, allaient trop vite, presque.",
        (1, 1, 2): "narrateur|L'ornière gardait le petit, presque.",
        (1, 1, 3): "narrateur|La pente prenait le grand, presque.",
        (1, 2, 1): "narrateur|Le couloir l'avalait, trop étroit, presque.",
        (1, 2, 2): "narrateur|La racine gardait le grain, presque.",
        (1, 2, 3): "narrateur|Les tiges se refermaient, trop tôt, presque.",
        (1, 3, 1): "narrateur|Les deux cerceaux montaient sans elle, presque.",
        (1, 3, 2): "narrateur|Le bois tombait dans le vide, presque.",
        (1, 3, 3): "narrateur|La dernière marche restait trop haute, presque.",
        (2, 1, 1): "narrateur|Sans ses mains, le petit restait au bord, presque.",
        (2, 1, 2): "narrateur|Sans le pont, le bleu manquait, presque.",
        (2, 1, 3): "narrateur|Deux vitesses se perdaient, presque.",
        (2, 2, 1): "narrateur|Sous l'herbe, le bleu restait, presque.",
        (2, 2, 2): "narrateur|Ses mains serraient trop, presque.",
        (2, 2, 3): "narrateur|Une tige claquait trop tôt, presque.",
        (2, 3, 1): "narrateur|Sans elle, il portait les deux, presque.",
        (2, 3, 2): "narrateur|Sans ses mains, elle ne recevait rien, presque.",
        (2, 3, 3): "narrateur|Trop vite, le seuil se fermait, presque.",
        (3, 1, 1): "narrateur|D'un coup, le bâton poussait trop, presque.",
        (3, 1, 2): "narrateur|Dans l'ornière, le pont glissait, presque.",
        (3, 1, 3): "narrateur|Avec la pente, le bâton partait, presque.",
        (3, 2, 1): "narrateur|Trop tôt, le passage se refermait, presque.",
        (3, 2, 2): "narrateur|Trop tôt, la racine retombait, presque.",
        (3, 2, 3): "narrateur|Sans le geste, l'herbe gardait le bâton, presque.",
        (3, 3, 1): "narrateur|Sans elle, le bâton finissait le seuil, presque.",
        (3, 3, 2): "narrateur|Trop tôt, le bois lui échappait, presque.",
        (3, 3, 3): "narrateur|Un seul pied prenait la brique, presque.",
    }[(a, b, c)]
    return arrive + body + [listen, pay] + gesture + [traces, almost]


def ending_lines(a: int, b: int, c: int) -> list[str]:
    firsts = {
        (1, 1, 1): "Devant la porte, le seuil de brique sent la poussière.",
        (1, 1, 2): "Derrière le pont, l'ornière s'est tue.",
        (1, 1, 3): "Deux cerceaux se touchent, contre le bois jaune.",
        (1, 2, 1): "Sous le tilleul, un couloir reste large comme Mila.",
        (1, 2, 2): "Une racine tient un peu de brique, collée.",
        (1, 2, 3): "Derrière leurs talons, les tiges se referment.",
        (1, 3, 1): "Contre le gond, le grand orange sèche.",
        (1, 3, 2): "Dans les mains de Mila, le bois reste chaud.",
        (1, 3, 3): "Sur la dernière marche, deux empreintes inégales.",
        (2, 1, 1): "Au bord du bleu, une virgule de poussière tient.",
        (2, 1, 2): "Sous le bois, le grain de brique brille.",
        (2, 1, 3): "Deux vitesses se sont rejointes, sur la terre.",
        (2, 2, 1): "Dans l'herbe, le couloir sent le petit bleu.",
        (2, 2, 2): "Une poudre rouge sèche, sur ses paumes.",
        (2, 2, 3): "Une tige pliée montre le passage, unique.",
        (2, 3, 1): "Mila a reçu le bleu, sur la marche haute.",
        (2, 3, 2): "Contre la porte jaune, le petit cerceau penche.",
        (2, 3, 3): "Deux souffles restent, sur la dernière brique.",
        (3, 1, 1): "Au bout du bâton, une poussière rouge tient.",
        (3, 1, 2): "Sur le pont du grand, une ligne rouge reste.",
        (3, 1, 3): "Entre les deux cerceaux, le bâton s'endort.",
        (3, 2, 1): "Pendant un saut, le bâton a tenu l'herbe.",
        (3, 2, 2): "Une racine a rendu le grain, au bois.",
        (3, 2, 3): "Voilà le bâton, une tige coincée, unique.",
        (3, 3, 1): "Contre le gond, le bâton tape, puis se tait.",
        (3, 3, 2): "Mila tient le bâton, plus petit que le gond.",
        (3, 3, 3): "Calée sur la marche, une brique garde le grain.",
    }
    lasts = {
        (1, 1, 1): "Sur le seuil, le grain de brique a retrouvé son trou.",
        (1, 1, 2): "Le pont du grand garde une virgule de poussière.",
        (1, 1, 3): "Les deux cerceaux se taisent, contre la porte jaune.",
        (1, 2, 1): "L'ombre du tilleul s'endort sur le couloir.",
        (1, 2, 2): "La racine sèche, sans le grain.",
        (1, 2, 3): "Derrière eux, l'herbe reprend sa place.",
        (1, 3, 1): "Le gond garde un peu d'orange, minuscule.",
        (1, 3, 2): "Les paumes de Mila gardent le bois.",
        (1, 3, 3): "Deux empreintes sèchent, inégales, sur la pierre.",
        (2, 1, 1): "Le petit bleu sèche, une virgule au bord.",
        (2, 1, 2): "Sous le pont, le grain de brique se tait.",
        (2, 1, 3): "La terre garde deux ronds, l'un plus lent.",
        (2, 2, 1): "Le couloir sent le bleu, puis plus.",
        (2, 2, 2): "Sur ses paumes, la poudre rouge s'endort.",
        (2, 2, 3): "La tige pliée veille, unique.",
        (2, 3, 1): "La marche haute garde le bleu, un instant.",
        (2, 3, 2): "Contre la porte, le petit penche, et tient.",
        (2, 3, 3): "Sur la dernière brique, deux souffles s'éteignent.",
        (3, 1, 1): "Au bout du bâton, la poussière rouge sèche.",
        (3, 1, 2): "La ligne rouge du pont s'efface, lente.",
        (3, 1, 3): "Entre les cerceaux, le bâton s'endort.",
        (3, 2, 1): "L'herbe rend le bâton, sans un bruit.",
        (3, 2, 2): "Le grain de brique a quitté la racine.",
        (3, 2, 3): "La tige coincée sèche, unique.",
        (3, 3, 1): "Le gond se tait, après le toc du bâton.",
        (3, 3, 2): "Dans ses mains, le bâton pèse moins.",
        (3, 3, 3): "Dans le trou du seuil, le grain de brique tient.",
    }
    qs = {
        1: "papa|Quel moment tu gardes, sur la terre ?",
        2: "maman|Quel moment tu gardes, dans l'herbe ?",
        3: "papa|Quel moment tu gardes, sur le perron ?",
    }[b]
    ans = {
        (1, 1, 1): "enfant-m|Quand ses mains ont dit non, d'abord.",
        (1, 1, 2): "enfant-m|Quand le petit a pris le pont.",
        (1, 1, 3): "enfant-m|Quand j'ai ralenti, jusqu'à son saut.",
        (1, 2, 1): "enfant-m|Quand le couloir s'est ouvert à sa taille.",
        (1, 2, 2): "enfant-m|Quand la racine a rendu le grain.",
        (1, 2, 3): "enfant-m|Quand elle a tiré sa tige.",
        (1, 3, 1): "enfant-m|Quand j'ai porté le mien, rien que le mien.",
        (1, 3, 2): "enfant-m|Quand elle a reçu le bois, prête.",
        (1, 3, 3): "enfant-m|Quand nos deux pieds ont pris la brique.",
        (2, 1, 1): "enfant-m|Quand j'ai attendu, au bord de l'ornière.",
        (2, 1, 2): "enfant-m|Quand le bleu a trouvé le pont.",
        (2, 1, 3): "enfant-m|Quand nos deux ronds ont tenu.",
        (2, 2, 1): "enfant-m|Quand le bleu a repris le couloir.",
        (2, 2, 2): "enfant-m|Quand mes mains ont tenu, sans serrer.",
        (2, 2, 3): "enfant-m|Quand la tige a gardé sa place.",
        (2, 3, 1): "enfant-m|Quand je n'ai pas pris les deux.",
        (2, 3, 2): "enfant-m|Quand elle a dit oui, avec les mains.",
        (2, 3, 3): "enfant-m|Quand nos souffles se sont rejoints.",
        (3, 1, 1): "enfant-m|Quand le bâton a cessé de pousser trop.",
        (3, 1, 2): "enfant-m|Quand le pont a tenu, sous le bleu.",
        (3, 1, 3): "enfant-m|Quand le bâton s'est calé, entre nous.",
        (3, 2, 1): "enfant-m|Quand le passage a attendu son saut.",
        (3, 2, 2): "enfant-m|Quand la racine a lâché, à temps.",
        (3, 2, 3): "enfant-m|Quand on a écarté, tige après tige.",
        (3, 3, 1): "enfant-m|Quand le bâton n'a pas fini sans elle.",
        (3, 3, 2): "enfant-m|Quand elle a pris le bois, plus tard.",
        (3, 3, 3): "enfant-m|Quand le grain a trouvé son trou.",
    }[(a, b, c)]
    mid = {
        1: "narrateur|Voilà le grand orange, le grain de brique au bois.",
        2: "narrateur|Voilà le petit bleu, voyageur du grain de brique.",
        3: "narrateur|Voilà le bâton, guide du grain de brique.",
    }[a]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        mid,
        "enfant-m|On est arrivés, les deux.",
        "enfant-f|Moi, j'ai pris mon temps.",
        qs,
        ans,
        "enfant-m|Je raconte le moment difficile, surtout.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{T1_META[a]['short']}_{T2_META[b]['short']}_{c}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "oiseau,bois,poussiere")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {
            "pause_before_ms": 200,
            "fields": {
                "option_1_label": "le grand cerceau",
                "option_2_label": "le petit cerceau",
                "option_3_label": "le bâton",
            },
        },
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            T1_META[a]["sons"],
            {"emphasis": T1_META[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"pause_before_ms": 200, "fields": Q_FIELDS[a]},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            T1_META[a]["sons"],
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {
                "pause_before_ms": 200,
                "fields": {
                    "option_1_label": "le chemin de terre",
                    "option_2_label": "l'herbe du tilleul",
                    "option_3_label": "le perron",
                },
            },
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                T2_META[b]["sons"],
                {"emphasis": T2_META[b]["short"]},
            )
            labs = T3_LABS[b]
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {
                    "pause_before_ms": 200,
                    "fields": {
                        "option_1_label": labs[0],
                        "option_2_label": labs[1],
                        "option_3_label": labs[2],
                    },
                },
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    T3_SONS[b][c],
                    {"emphasis": "grain de brique"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "porte,bois",
                    {"emphasis": "grain de brique", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = [out_chunks[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    lasts = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in out_chunks[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

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

    blob = "\n".join(c["script"] for c in out_chunks.values()).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment x{blob.count('en ce moment')}")
    if "grain de brique" not in out_chunks["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    joined_scripts = "\n".join(c["script"] for c in out_chunks.values())
    adults_n = sum(
        1
        for ln in joined_scripts.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    )
    if adults_n < 8:
        raise SystemExit(f"trop peu d'adultes: {adults_n}")
    merci_n = sum(
        1
        for ln in "\n".join(c["script"] for c in out_chunks.values()).splitlines()
        if ln.startswith(("papa|", "maman|")) and "merci" in ln.lower()
    )
    if merci_n != 1:
        raise SystemExit(f"merci vécu ×{merci_n}, voulu 1")
    for c in src["chunks"]:
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"] and not c["chunk_id"].endswith("T0003_P0000"):
            if "grain de brique" not in out_chunks[c["chunk_id"]]["text"].lower():
                raise SystemExit(f"indice non payé: {c['chunk_id']}")
        if c["kind"] == "passage_fin":
            if "grain de brique" not in out_chunks[c["chunk_id"]]["text"].lower():
                raise SystemExit(f"indice absent de la fin: {c['chunk_id']}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Mila saute, Aniss pousse : deux rythmes, une porte jaune. "
        "Un grain de brique s'est coincé dans le cerceau orange ; le seuil "
        "a un trou de la même taille. Aniss veut les deux cerceaux au bois "
        "jaune, tout de suite. Il pousse trop vite : le grand part, le petit "
        "reste. Mila ne dit rien. Papa s'accroupit. Grand, petit ou bâton : "
        "les trois partent. Terre, herbe du tilleul ou perron : une pente, "
        "un couloir, une marche veulent le laisser seul. Il refuse de foncer. "
        "Mains, pont, rouler, couloir, écarter, porter, recevoir, dernière "
        "marche : le grain retrouve son trou. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Aniss, Mila, papa, maman"
    merged["setting"] = "chemin du village : terre, herbe du tilleul, perron"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    if min(counts) < 550 or max(counts) > 700:
        raise SystemExit(f"chemin hors barre 550-700: min {min(counts)} max {max(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types "
        "de blocs et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Mila saute sur un pied, face à la porte jaune. Aniss tient le cerceau "
        "orange. Un grain de brique s'est coincé dans le bois ; le seuil a un "
        "trou de la même taille. Aniss veut les deux cerceaux jusqu'à la porte, "
        "tout de suite. Il pousse trop vite : le grand part, le petit reste. "
        "Mila ne dit rien. Son silence tient, comme une réponse. Le sourire "
        "disparaît. Papa s'accroupit : sans elle, ou avec elle ? Grand, petit "
        "ou bâton : les trois partent. Terre, herbe du tilleul ou perron : une "
        "pente, un couloir, une marche veulent le laisser seul. Il refuse de "
        "foncer. Le grain retrouve son trou. Les cerceaux portent une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chemin du village, seuil de brique, porte jaune.\n"
        "- Désir : faire arriver les deux cerceaux à la porte, avec Mila.\n"
        "- Objet : grand cerceau orange (grain de brique), petit bleu, bâton.\n"
        "- Indice unique : le grain de brique, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : le grain doit retrouver le trou du seuil, au soleil.\n"
        "- Imprévu 1 : Aniss pousse trop vite ; le grand tombe, Mila reste.\n"
        "- Cue : papa s'accroupit. Un merci vécu (tu l'as attendue).\n"
        "- Imprévu 2 (plus rusé) : pente, couloir, marche qui finiraient sans elle.\n"
        "- Revers : silence de Mila, corps, refus de foncer, grain retrouvé.\n"
        "- Résolution : mains, pont, rouler, couloir, écarter, porter, recevoir, marche.\n"
        "- Retour : grain dans le trou, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (deux rythmes face à la porte), pas un gabarit v2.\n"
        "- Le premier choix n'enlève pas l'équipement : les trois affaires partent.\n"
        "- Déclencheur : les deux enfants ne veulent pas la même chose au même moment.\n"
        "- Silence de Mila = réponse. Rythmes distincts, sans voix caricaturale.\n"
        "- Neuf obstacles T2, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon DIF.COR.001 vécue (avancer avec l'autre, respecter son rythme), jamais dite.\n"
        "- Monde ≠ TREE-DIF-044 groseilles/treillis, ≠ TREE-DIF-056 statue/bronze, "
        "≠ TREE-DIF-045 école/galet/poisson.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Aniss, Mila, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience d'Aniss au départ, petit découragement quand le cerceau tombe "
        "ou que Mila s'arrête, fierté calme quand il refuse de foncer. "
        "L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N2 ≤ 15 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
