#!/usr/bin/env python3
"""ATOM-EMO.GES.001-03 — Nina dit stop au parc (F-NAR-019, N2, EMO.GES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.001-03"
TITLE = "Nina dit stop au parc"
N2 = LIMITS["N2"]
CHARS = "Nina, Raphaël, papa, maman"
SETTING = (
    "parc, toboggan, herbe, soleil, sac, jaune, vent, "
    "poussière, marches"
)
INDICE = "éclat de toboggan"
FIL = (
    "Le soleil tient le jaune. Près du sac, un éclat de "
    "toboggan brille. Nina veut glisser, maintenant. Raphaël "
    "ouvre les bras, serre trop. Sourire parti, poitrine, "
    "maman accroupie. Stop, recule. Merci vécu. Deuxième ruse : "
    "un câlin au pied. Un éclat de toboggan tient sur le jaune."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|piquet|portail|rotin|crochet|platane|cageot|résine|"
    r"resine|botte|bottes|limace|perron|chaise|tiroir|fraisier|"
    r"cuivre|buis|cerceau|grille|cour|pierre|nappe|figue|robinet|"
    r"planche|émail|email|samare|bassine|lunettes|corde|drap|"
    r"ballon|entrée|entree|horloge|bol|casserole|soupe|"
    r"chiffon|sauge|lacet|commode|gond|banc|coussin|confiture|"
    r"tartine|fraise|parquet|tapis|camion|seau|sable|pelle|"
    r"gourde|oiseau|balançoire|balancoire|rideau|moineau|trèfle|"
    r"trefle|clôture|cloture|papillon|colline|miel)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "on peut jouer",
    "on peut attendre",
    "on peut demander",
    "on peut laisser le temps",
    "laisser le temps",
    "on attend la fin",
    "on écoute jusqu'au bout",
    "laisse-le finir",
    "laisse le finir",
    "on n'interrompt",
    "on n interrompt",
    "n'interrompt pas",
    "on n'achève pas",
    "finir sa phrase",
    "fin de la phrase",
    "tu as su attendre",
    "vous avez laissé le temps",
    "vous parlez bien",
    "ce n'est pas une faute",
    "n'est pas une faute",
    "pas une faute",
    "vous jouez",
    "on joue",
    "parle peu",
    "elle parle peu",
    "forcer la parole",
    "on ne force pas",
    "regarder, c'est",
    "on n'imite pas",
    "on n imite pas",
    "cherche un mot",
    "dire stop, c'est permis",
    "dire stop c'est permis",
    "on s'éloigne",
    "on s eloigne",
    "on va vers un adulte",
    "tu as dit stop",
    "c'est le bon geste",
    "c est le bon geste",
    "tu t'es éloigné",
    "tu t'es éloignée",
    "tu t es eloigne",
    "on peut dire stop",
    "il faut dire stop",
    "tu as le droit",
    "on s'éloigne vers",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sève",
    "éclat de seve",
    "éclat de botte",
    "éclat de limace",
    "éclat de perron",
    "éclat de chaise",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de casserole",
    "éclat de citron",
    "éclat de coquille",
    "éclat de zeste",
    "éclat de coussin",
    "éclat de figue",
    "éclat de robinet",
    "éclat de planche",
    "éclat de cerceau",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de nappe",
    "éclat de farine",
    "éclat de tablier",
    "éclat de biscuit",
    "éclat de toit",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de seau",
    "éclat de pompon",
    "éclat de carton",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de ballon",
    "éclat de manteau",
    "éclat de marche",
    "éclat de vitre",
    "éclat de grain",
    "éclat de liste",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de couloir",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de thermos",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat de lessive",
    "éclat de carreau",
    "éclat de coton",
    "éclat de gravier",
    "éclat de gilet",
    "éclat de lunettes",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de portail",
    "éclat de rotin",
    "éclat de crochet",
    "éclat de platane",
    "éclat de cageot",
    "éclat de résine",
    "éclat de resine",
    "éclat de carte",
    "éclat de tapis",
    "éclat de vapeur",
    "éclat de bol",
    "éclat de chiffon",
    "éclat de sauge",
    "éclat de lacet",
    "éclat de commode",
    "éclat de gond",
    "éclat de banc",
    "éclat de parquet",
    "éclat de rond",
    "éclat de table",
    "éclat de pain",
    "éclat de papier",
    "éclat de dessin",
    "éclat de bateau",
    "éclat de sel",
    "éclat d'horloge",
    "éclat d horloge",
    "éclat de carotte",
    "éclat de pupitre",
    "éclat de plateau",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de rideau",
    "éclat de plaid",
    "éclat de sac",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de toboggan",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis serrement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_glisser_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Nina",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=c_est_trop_que_dit_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Stop",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis air_qui_revient; intensite=2; "
            "destinataire=enfant; sous_texte=elle_dit_stop_elle_recule; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de toboggan",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=calin_au_pied_elle_recule_encore; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de toboggan",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_air_libre; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_jaune; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": None,
    "accepted_examples": None,
    "retry_prompt": None,
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Le soleil pose une bande chaude sur le jaune.",
            "narrateur|L'herbe sent l'été, au parc.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Tu le sens, l'herbe, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le toboggan jaune tient le soleil.",
            "narrateur|Une poussière d'été danse au bord.",
            "enfant-f|Il est jaune, maman.",
            "maman|Tu le vois, le toboggan ?",
            "enfant-f|Oui, maman.",
            "narrateur|Près du sac, un éclat de toboggan brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Maman pose le sac dans l'herbe.",
            "narrateur|Le tissu est chaud, un peu rêche.",
            "enfant-f|Il est chaud.",
            "maman|Tu veux un coin d'ombre ?",
            "enfant-f|Oui.",
            "narrateur|Nina touche le jaune du toboggan.",
            "narrateur|Le plastique est tiède, lisse.",
            "papa|Le jaune tient chaud, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Nina tient le bord.",
            "narrateur|Ses pieds veulent les marches.",
            "enfant-f|Je veux glisser, maintenant !",
            "enfant-f|Sur le toboggan, tout de suite.",
            "papa|Le toboggan, là ?",
            "enfant-f|Oui, le toboggan.",
            "maman|Tes mains tiennent le bord, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Raphaël arrive dans l'herbe.",
            "narrateur|Il ouvre les bras tout grand.",
            "copain|Nina !",
            "copain|Un câlin !",
            "enfant-f|Je glisse, maintenant !",
            "narrateur|Nina avance trop vite vers lui.",
            "narrateur|Raphaël la serre contre sa poitrine.",
            "narrateur|Le câlin est trop fort.",
            "enfant-f|Oh.",
            "narrateur|Nina connaît le toboggan.",
            "narrateur|Elle veut les marches.",
            "narrateur|Les bras serrent trop près.",
            "copain|Viens !",
            "narrateur|Raphaël serre plus fort, content.",
            "narrateur|Nina ne peut plus bouger.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'air se coince.",
            "narrateur|Ses épaules montent un peu.",
            "narrateur|Maman s'accroupit à la même hauteur.",
            "maman|Tu vois Raphaël, Nina ?",
            "enfant-f|Oui, maman.",
            "papa|Les bras sont trop près, Nina ?",
            "enfant-f|Un peu, papa.",
            "narrateur|L'éclat de toboggan tremble, puis tient.",
            "narrateur|Raphaël baisse les yeux.",
            "enfant-f|Je ne peux plus, maman.",
            "narrateur|Nina regarde maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|C'est trop pour Nina.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Nina veut glisser, tout de suite.",
            "enfant-f|Je pars, maintenant !",
            "narrateur|Elle tire vers les marches.",
            "narrateur|Les bras restent collés.",
            "narrateur|Raphaël serre, sans le vouloir.",
            "narrateur|L'air manque dans sa poitrine.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nina refuse de rester prise.",
            "enfant-f|Stop.",
            "narrateur|Elle recule d'un pas.",
            "narrateur|Les bras s'ouvrent.",
            "narrateur|L'air revient, chaud.",
            "maman|Tu veux de la place, Nina ?",
            "narrateur|Maman reste à la même hauteur.",
            "enfant-f|Maman, on fait quoi ?",
            "maman|On reste un peu, puis on glisse.",
            "enfant-f|D'accord.",
            "narrateur|Nina reste un moment, les mains ouvertes.",
            "narrateur|Elle garde un pas d'herbe.",
            "copain|Pardon.",
            "enfant-f|C'est trop.",
            "narrateur|Raphaël hoche la tête.",
            "narrateur|Nina pose une main sur le sac.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux, dans l'herbe.",
            "maman|Le jaune est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "narrateur|Papa tend le bord du toboggan.",
            "narrateur|Nina touche.",
            "narrateur|C'est lisse et chaud.",
            "narrateur|Raphaël touche aussi.",
            "enfant-f|Le toboggan.",
            "papa|Il a des marches, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Nina glisse la main sur le jaune.",
            "narrateur|Le plastique est lisse, contre la peau.",
            "maman|Tes mains sont au chaud, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Raphaël pose un doigt sur le bord.",
            "copain|Jaune.",
            "enfant-f|On y va, après ?",
            "maman|Le sac est près du toboggan.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Ils restent près du toboggan.",
            "narrateur|Nina pose un pied sur la marche.",
            "copain|On y va ensemble !",
            "enfant-f|Je glisse, maintenant !",
            "narrateur|Raphaël ouvre les bras trop vite.",
            "narrateur|Il la serre pour monter.",
            "enfant-f|Oh.",
            "narrateur|Nina avance les pieds, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Nina refuse de rester prise, cette fois.",
            "narrateur|Sa poitrine se serre, puis s'ouvre.",
            "enfant-f|Stop.",
            "narrateur|Elle recule d'un pas.",
            "narrateur|Personne ne serre plus.",
            "narrateur|Elle observe le jaune, un instant.",
            "narrateur|Elle écoute le vent du parc.",
            "narrateur|Au pied, un éclat de toboggan luit.",
            "enfant-f|Là, sur le jaune.",
            "enfant-f|Tu montes après, Raphaël ?",
            "narrateur|Raphaël ne serre plus.",
            "narrateur|Il tient le bord, sans coller.",
            "copain|Après toi.",
            "narrateur|Nina recule un peu, sans se presser.",
            "narrateur|Raphaël pose les mains, plus lentement.",
            "narrateur|Le plastique est lisse et tiède.",
            "papa|Tu la vois, la marche ?",
            "enfant-f|Oui, papa.",
            "maman|Le sac est près du jaune ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le toboggan tient contre le soleil.",
            "narrateur|Nina pose une main sur le bord.",
            "narrateur|Raphaël pose la suivante.",
            "papa|Le jaune tient, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Le vent passe sur l'herbe.",
            "enfant-f|Il chatouille les genoux.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du jaune.",
            "maman|Le toboggan est à toi, Nina ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina souffle, un filet d'air.",
            "enfant-f|L'herbe sent bon.",
            "maman|Tu le sens, le parc ?",
            "enfant-f|Oui, maman.",
            "papa|La glisse reste un peu, chaude.",
            "enfant-f|Elle a tenu, sous les mains.",
            "copain|Toboggan.",
            "narrateur|L'herbe est chaude, sous les mains.",
            "narrateur|Le jaune fait une ombre ronde.",
            "enfant-f|On glisse, après.",
            "narrateur|Un éclat de toboggan tient sur le jaune.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_lesson = cid == "CHK_T0000_P0000_Q0001"
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_lesson:
            for bad in EXTRA_BAD:
                if bad in low:
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copain"):
            raise SystemExit(f"rôle {role}: {raw}")
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
    cid = src.get("chunk_id") or ""
    lines = vet(lines, cid)
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
    return out


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in SCRIPTS]
    extra = set(SCRIPTS) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        profile, sons, lines = SCRIPTS[cid]
        extra_kw: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra_kw["pause_before_ms"] = 200
            extra_kw["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra_kw["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra_kw)
        if c.get("kind") != by[cid].get("kind"):
            raise SystemExit(f"{cid}: kind changé")
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit(f"{SID}: bravo en trop")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "stop" not in blob:
        raise SystemExit(f"{SID}: manque stop")
    if "recule" not in blob:
        raise SystemExit(f"{SID}: manque recule")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f, Raphaël = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copain") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copain" for r in roles):
        raise SystemExit(f"{SID}: copain absent")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "dire stop, c'est permis",
        "dire stop c'est permis",
        "on s'éloigne",
        "on va vers un adulte",
        "tu as dit stop",
        "c'est le bon geste",
        "tu t'es éloigné",
        "tu t'es éloignée",
        "on peut dire stop",
        "il faut dire stop",
        "tu as le droit",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "l'histoire est finie",
        "mission accomplie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "C'est trop pour Nina. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer inventé")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples inventé")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry inventé")
    if "toboggan" not in blob:
        raise SystemExit(f"{SID}: manque toboggan")
    if "herbe" not in blob:
        raise SystemExit(f"{SID}: manque herbe")
    if "sac" not in blob:
        raise SystemExit(f"{SID}: manque sac")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if re.search(r"\bbanc\b", blob):
        raise SystemExit(f"{SID}: BAN banc")
    if re.search(r"\bcour\b", blob):
        raise SystemExit(f"{SID}: BAN cour")
    if re.search(r"\bgrille\b", blob):
        raise SystemExit(f"{SID}: BAN grille")
    for ban in (
        "éclat de balançoire",
        "éclat de rideau",
        "éclat de banc",
        "éclat de plaid",
        "éclat de carotte",
        "tout doux",
        "tout calme",
        "fatou",
        "chouchou",
        "côme",
        "come ",
        "victorina",
        "sarah",
        "amir",
        "kenzo",
        "maya",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in chunks
    )
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (≤15 mots/phrase), audio familial\n"
        "- **Leçon :** EMO.GES.001 — trop fort → stop, reculer (vécue : "
        "câlin trop fort, poitrine coincée, sourire parti, maman "
        "accroupie, Nina dit stop, recule d'un pas, air qui revient, "
        "puis câlin au pied du toboggan, stop, recule). JAMAIS dite "
        "dans le récit. Pas « dire stop, c'est permis ». Pas « on "
        "s'éloigne ». Pas « on va vers un adulte ».\n"
        "- **Personnages :** Nina, Raphaël, papa, maman. Dump Fatou/"
        "Côme/Chouchou/Victorina → D16. Nina = enfant-f (veut glisser "
        "maintenant, serre trop, dit stop, recule). Raphaël = copain "
        "(câlin trop fort, viens, on y va ensemble, pardon, après "
        "toi). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** parc, toboggan, herbe, soleil, sac, jaune, vent, "
        "poussière, marches. ≠ GES.001-01 banc / balançoire. ≠ "
        "GES.001-02 rideau. ≠ dump banc / cour / grille / portail.\n"
        "- **Indice unique :** éclat de toboggan (brille à l'ouverture "
        "près du sac sous le soleil, tremble au câlin trop fort → "
        "luit au refus du pied → tient sur le jaune). BAN éclat de "
        "balançoire (001-01) / rideau (001-02) / banc / plaid.\n"
        "- **Question moteur :** « C'est trop pour Nina. Que dit-elle ? » "
        "expected / accepted / retry **null** (consigne, non inventés). "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le soleil tient le jaune. Près du sac, un éclat de toboggan "
        "brille. Nina veut glisser **maintenant**. Raphaël ouvre les "
        "bras, serre trop. Sourire parti. Poitrine coincée. Maman "
        "s'accroupit. Elle dit stop. Elle recule. Merci vécu. "
        "Deuxième ruse : un câlin au pied, pour monter ensemble. Elle "
        "s'arrête, lit l'éclat. Un éclat de toboggan tient sur le "
        "jaune.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc, toboggan, herbe, soleil, sac, jaune. ≠ "
        "001-01 banc / balançoire. ≠ 001-02 rideau. ≠ dump portail / "
        "moineau / miel.\n"
        "- Désir : glisser, maintenant, sur le toboggan.\n"
        "- Objet : toboggan jaune, sac, marches, éclat.\n"
        "- Indice unique : éclat de toboggan, vu dès l'ouverture près "
        "du sac, payé sur le jaune. Pas éclat de balançoire / rideau / "
        "banc.\n"
        "- Urgence douce : Raphaël arrive, Nina accélère vers le "
        "câlin et les marches.\n"
        "- Imprévu 1 : Raphaël serre trop. Poitrine coincée. Sourire "
        "parti. Elle tire vers les marches, les bras restent collés.\n"
        "- Cue : maman à la même hauteur. Un merci vécu, après le "
        "geste.\n"
        "- Imprévu 2 (plus rusé) : au pied, « on y va ensemble », "
        "câlin pour monter.\n"
        "- Résolution : elle dit stop, recule, observe, écoute, garde "
        "un pas.\n"
        "- Retour : glisse chaude, herbe, éclat sur le jaune.\n\n"
        "## Vécu\n\n"
        "Nina veut glisser **maintenant**. Impatience, puis câlin trop "
        "fort, sourire parti. Raphaël pose sa limite à l'envers "
        "(bras, viens, ensemble). Maman se baisse, pose une question, "
        "ne récite pas la règle. Elle agit : stop, reculer. Merci "
        "vécu. Fin : l'éclat du début tient sur le jaune.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nina dit stop au parc (noyau dump, prénom D16). "
        "Relance : Que dit-elle ? expected null.\n"
        "- Lieu du dump (parc, toboggan, herbe) sans banc / cour / "
        "grille. Papa présent. Raphaël = copain.\n"
        "- Ouverture inventée (soleil sur le jaune), pas un gabarit "
        "v2, pas « Le portail du parc grince » du dump en première "
        "ligne.\n"
        "- Indice unique : éclat de toboggan. BAN éclat de "
        "balançoire / rideau / banc / plaid. Pas tache/flèche/marque/"
        "symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » / « encore » / « banc » "
        "du dump.\n"
        "- Leçon non dite : on la voit quand le câlin serre, quand "
        "Nina dit stop, quand elle recule, quand l'air revient. Pas "
        "« dire stop, c'est permis ». Pas « on va vers un adulte ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « C'est trop pour Nina. Que dit-elle ? ». "
        "expected / accepted / retry laissés null. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 040 / 072 / 004 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_002_01.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le pied du toboggan.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
