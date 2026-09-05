#!/usr/bin/env python3
"""ATOM-DIF.COR.001-08 — Le train de coussins de Sarah (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-08"
TITLE = "Le train de coussins de Sarah"
N1 = LIMITS["N1"]
INDICE = "éclat de coussin"
CHARS = "Sarah, Victorino, papa, maman"
SETTING = (
    "salon puis porte du jardin, vapeur de soupe, cuillère, "
    "thym, canapé, coussins"
)
FIL = (
    "La vapeur colle à la vitre. Une cuillère attend. Ça sent le "
    "thym. Sur le tissu, un éclat de coussin brille. Sarah veut un "
    "train de coussins jusqu'à la porte, maintenant, pour la lune. "
    "Elle tire trop vite, seule : le troisième reste coincé, le train "
    "n'atteint pas. Victorino attend, puis soulève. Elle refuse de "
    "foncer. Merci vécu. Le loquet est haut. Un éclat de coussin "
    "reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(figue|robinet|planche|cerceau|émail|email|samare|bassine|"
    r"fraise|plaid|cerisier|carton|tilleul|ballon|pomme|drap)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "louise",
    "miel",
    "merle",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "voisine",
    "tout chaud",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "on aime écouter",
    "même leçon",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "tailles différentes",
    "on peut jouer ensemble",
    "vous jouez ensemble",
    "on a joué ensemble",
    "vous avez joué ensemble",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "éclat de figue",
    "éclat de poire",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de casier",
    "éclat de laine",
    "éclat de marche",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de crayon",
    "éclat de croûte",
    "éclat de croute",
    "éclat de seau",
    "éclat de tomate",
    "éclat de bâche",
    "éclat de bache",
    "éclat de samare",
    "éclat de bassine",
    "éclat de cerceau",
    "éclat d'émail",
    "éclat d'email",
    "éclat de carton",
    "éclat de bol",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de vitre",
    "éclat de tapis",
    "éclat de lampe",
    "éclat de table",
    "éclat de porte",
    "éclat de loquet",
    "éclat de thym",
    "éclat de soupe",
    "éclat de canapé",
    "éclat de canape",
)


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de coussin",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_train_jusqu_a_la_porte_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Victorino",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=sarah_invite_ils_tirent_le_coussin_ensemble; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="coussin",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_tirage_seul_echoue_le_coussin_sort_a_deux; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de coussin",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de coussin",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer ensemble",
    "accepted_examples": (
        "jouer ensemble | ensemble | ils jouent | on joue | jouer | le train"
    ),
    "retry_prompt": "Ils jouent ensemble. Que font Sarah et Victorino ?",
    "engine_ok_text": "Oui, jouer ensemble.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "soupe,coussin",
        [
            "narrateur|La vapeur de la soupe colle à la vitre.",
            "narrateur|Elle fait un nuage, un peu flou.",
            "enfant-f|On dirait un nuage, papa.",
            "papa|Tu l'as vue, Sarah ?",
            "narrateur|Une cuillère en bois attend.",
            "narrateur|Ça sent le thym, près du nez.",
            "maman|C'est le thym, dans la soupe.",
            "enfant-f|Ça sent bon, maman.",
            "narrateur|Le canapé a trois coussins.",
            "narrateur|Le tapis est un peu rêche.",
            "enfant-f|Il gratte, le tapis.",
            "papa|Tu as les genoux dessus ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un papillon de nuit tape la lampe.",
            "narrateur|La lampe fait un cercle pâle.",
            "enfant-f|Il tape, maman.",
            "maman|Il cherche la lumière.",
            "narrateur|Sur le tissu, un éclat de coussin brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, sur le tissu ?",
            "enfant-f|Oui, il brille.",
            "narrateur|Sarah touche l'éclat de coussin.",
            "narrateur|Le tissu est doux, un peu lourd.",
            "enfant-f|Il est doux.",
            "enfant-f|Je veux un train, maintenant !",
            "maman|Un train de coussins ?",
            "enfant-f|Oui.",
            "enfant-f|Jusqu'à la porte.",
            "papa|Pour voir le jardin ?",
            "enfant-f|Pour voir la lune.",
            "narrateur|En ce moment, Sarah tire un coussin.",
            "narrateur|Elle le pose vers la porte.",
            "narrateur|Le tissu fait un petit bruit.",
            "enfant-f|Un autre !",
            "narrateur|Sarah pose le deuxième, trop vite.",
            "narrateur|Le troisième manque.",
            "enfant-f|Il est où ?",
            "maman|Regarde sous la table.",
            "narrateur|Le coussin est coincé, sous le bois.",
            "narrateur|Sarah tend le bras, toute seule.",
            "narrateur|Ses doigts touchent le tissu.",
            "narrateur|Le coussin ne vient pas.",
            "enfant-f|Oh.",
            "narrateur|Le train s'arrête, trop court.",
            "narrateur|Il n'atteint pas la porte.",
            "enfant-f|Il n'arrive pas !",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Les épaules de Sarah tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "enfant-f|Je le prends !",
            "narrateur|Sarah tire trop fort, d'un coup.",
            "narrateur|Le tissu reste coincé.",
            "papa|Tu le vois, Sarah ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Victorino arrive du couloir.",
            "narrateur|Ses chaussettes glissent un peu.",
            "narrateur|Il est plus grand, près de la table.",
            "narrateur|Sarah est plus petite, sous le bois.",
            "enfant-f|Tu veux le train ?",
            "narrateur|Victorino ne dit rien, d'abord.",
            "narrateur|Il regarde le coussin, puis Sarah.",
            "enfant-m|Oui.",
            "enfant-f|Viens.",
            "narrateur|Ils se mettent à quatre pattes.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah invite Victorino.",
            "narrateur|Que font-ils ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "table,coussin",
        [
            "narrateur|Sarah veut le coussin, toute seule.",
            "enfant-f|Je le prends, maintenant !",
            "narrateur|Elle avance trop vite sous la table.",
            "narrateur|Le tissu reste coincé.",
            "enfant-f|Oh.",
            "narrateur|Victorino veut soulever trop haut.",
            "enfant-m|Je pousse fort.",
            "narrateur|La table penche un peu.",
            "narrateur|Le coussin recule.",
            "enfant-m|Il ne vient pas.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme les mains.",
            "narrateur|Elle écoute le salon, un instant.",
            "papa|Tu veux venir près de la table ?",
            "narrateur|Papa reste à la même hauteur.",
            "narrateur|Sarah pose un genou sur le tapis.",
            "narrateur|Le tapis est rêche, un peu.",
            "enfant-f|Tu soulèves un peu ?",
            "narrateur|Victorino attend, puis prend le bord.",
            "enfant-m|Oui.",
            "narrateur|Il soulève un peu la table.",
            "narrateur|Sarah tire le coussin, tout près.",
            "narrateur|Le coussin sort, un peu plat.",
            "enfant-f|Je l'ai !",
            "enfant-m|Oui.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, près du bois.",
            "narrateur|Le ventre de Sarah se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au chaud ?",
            "enfant-f|Un peu, maman.",
            "papa|Victorino, tu tiens le bord ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils posent le troisième coussin.",
            "narrateur|Le train va jusqu'à la porte.",
            "enfant-f|Tout le monde à bord.",
            "enfant-m|Moi devant.",
            "enfant-f|Moi au milieu.",
            "narrateur|Ils s'assoient sur le tissu.",
            "narrateur|Le tapis gratte un peu.",
            "enfant-f|Toc, toc.",
            "enfant-m|Le train part.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "porte,jardin",
        [
            "narrateur|Sarah veut la porte, d'un coup.",
            "enfant-f|J'ouvre, maintenant !",
            "narrateur|Elle pousse le dernier coussin trop vite.",
            "narrateur|Le train s'arrête avant la porte.",
            "enfant-f|Oh.",
            "enfant-m|Il manque.",
            "narrateur|Le loquet est un peu haut.",
            "narrateur|Sarah saute vers le loquet.",
            "narrateur|Ses doigts n'arrivent pas.",
            "enfant-f|Il est trop haut !",
            "narrateur|Sarah avance les mains.",
            "narrateur|Puis elle s'arrête net.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Victorino attend, sans parler.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Sarah observe le tissu, écoute la porte.",
            "narrateur|Sur le tissu, un éclat de coussin luit.",
            "enfant-f|Là, sur le tissu.",
            "narrateur|Sarah tient le coussin des deux mains.",
            "enfant-f|Tu tournes le loquet ?",
            "enfant-m|Oui.",
            "narrateur|Victorino tourne le loquet, plus haut.",
            "narrateur|Sarah pousse le dernier coussin.",
            "narrateur|La porte s'ouvre un peu.",
            "narrateur|L'air du jardin entre.",
            "enfant-f|La lune !",
            "enfant-m|Elle est ronde.",
            "papa|Tu la vois, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|On avance ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un peu d'air touche les cheveux.",
            "enfant-f|Elle est froide, la lune.",
            "papa|On reste un moment.",
            "narrateur|Ils restent sur le dernier coussin.",
            "narrateur|La lune éclaire le seuil.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "vapeur",
        [
            "enfant-f|La vitre brillait, papa.",
            "papa|Tu la vois, comme sur le tissu ?",
            "enfant-f|Oui, dans la vapeur.",
            "narrateur|Sarah pose un coussin sur le canapé.",
            "maman|On le remet ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Le thym sentait bon.",
            "maman|Il est derrière nous.",
            "narrateur|La vapeur a quitté la vitre.",
            "narrateur|Sarah respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "enfant-m|À demain.",
            "enfant-f|À demain.",
            "narrateur|Les joues de Sarah se réchauffent.",
            "narrateur|Victorino pose les deux autres.",
            "narrateur|Un éclat de coussin reste pâle.",
        ],
    ),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
        b = BAN_WORDS.search(low)
        if b:
            raise SystemExit(f"interdit {b.group(0)!r}: {ph}")
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
    if "maman|" not in blob:
        raise SystemExit(f"{SID}: maman absente")
    if "papa|" not in blob:
        raise SystemExit(f"{SID}: papa absent")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "tout chaud" in blob:
        raise SystemExit(f"{SID}: BAN tout chaud")
    if "figue" in blob:
        raise SystemExit(f"{SID}: BAN figue (001-07)")
    if "robinet" in blob:
        raise SystemExit(f"{SID}: BAN robinet (001-05)")
    if "planche" in blob:
        raise SystemExit(f"{SID}: BAN planche (001-06)")
    if "cerceau" in blob:
        raise SystemExit(f"{SID}: BAN cerceau (001-04)")
    if "émail" in blob or "email" in blob:
        raise SystemExit(f"{SID}: BAN émail (001-01)")
    if "samare" in blob:
        raise SystemExit(f"{SID}: BAN samare (001-02)")
    if "bassine" in blob:
        raise SystemExit(f"{SID}: BAN bassine (001-03)")
    if "tout doux" in blob or "tout calme" in blob:
        raise SystemExit(f"{SID}: tic tout doux/calme")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Sarah invite Victorino. Que font-ils ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer ensemble":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "sarah" not in retry or "victorino" not in retry:
        raise SystemExit(f"{SID}: retry sans Sarah/Victorino")
    if "jouent ensemble" not in retry:
        raise SystemExit(f"{SID}: retry sans jouent ensemble")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain au lieu d'enfant-m")

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
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.001 — jouer ensemble "
        "(vécue : Sarah trop vite sous la table ; Victorino trop haut ; "
        "il soulève, elle tire ; le loquet trop haut, il tourne, elle pousse)\n"
        "- **Personnages :** Sarah, Victorino, papa, maman. Papa ajouté. "
        "Victorino = enfant-m (rythme lent, silence). Troupe D16. "
        "Pas de maîtresse.\n"
        "- **Lieu :** salon puis porte du jardin, vapeur de soupe, "
        "cuillère, thym, canapé, coussins. Strip « tout chaud ». "
        "≠ 001-01 émail / robinet. ≠ 001-02 samare. ≠ 001-03 bassine. "
        "≠ 001-04 cerceau. ≠ 001-05 robinet. ≠ 001-06 planche. "
        "≠ 001-07 figue.\n"
        "- **Indice unique :** éclat de coussin (brille à l'ouverture, "
        "touché, luit au refus, reste pâle)\n"
        "- **Question moteur :** « Sarah invite Victorino. Que font-ils ? » "
        "expected **jouer ensemble**.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La vapeur de la soupe colle à la vitre. Une cuillère en bois "
        "attend. Ça sent le thym. Sur le tissu, un éclat de coussin "
        "brille. Sarah veut un train jusqu'à la porte **maintenant**, "
        "pour la lune. Première idée : tirer seule, trop vite. Le "
        "troisième coussin reste coincé. Le train n'atteint pas. Sourire "
        "parti, épaules basses. Victorino arrive, plus grand, et attend. "
        "Elle refuse de foncer. Il soulève, elle tire. Merci vécu. Elle "
        "veut la porte d'un coup : le train s'arrête, le loquet est haut. "
        "Elle s'arrête, lit l'éclat. Un éclat de coussin reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, vapeur, cuillère, thym, canapé, tapis rêche, "
        "papillon de nuit, porte du jardin. Strip tout chaud.\n"
        "- Désir : le train de coussins jusqu'à la porte, pour la lune, "
        "maintenant.\n"
        "- Objet : trois coussins, table, loquet, vapeur, cuillère.\n"
        "- Indice unique : éclat de coussin, vu dès l'ouverture, payé pâle. "
        "Pas figue, robinet, planche, cerceau, émail, samare, bassine.\n"
        "- Urgence douce : le train trop court, la lune derrière la porte.\n"
        "- Imprévu 1 : tirer seule ; coussin coincé ; train qui n'atteint "
        "pas l'endroit promis.\n"
        "- Cue : papa à la même hauteur, près de la table. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : pousser le dernier coussin d'un coup ; "
        "loquet trop haut pour Sarah.\n"
        "- Résolution : elle refuse de foncer, Victorino tourne le loquet, "
        "elle pousse le coussin.\n"
        "- Retour : vapeur partie, thym derrière eux, éclat de coussin "
        "pâle, lune sur le seuil.\n\n"
        "## Vécu\n\n"
        "Sarah veut le train **maintenant**. Impatience, puis sourire qui "
        "disparaît. Victorino prend son temps, pose sa limite (silence, "
        "oui, moi devant). Papa se baisse, pose une question, ne récite "
        "pas la règle. Ils agissent : table soulevée, coussin tiré, "
        "loquet tourné, dernier coussin poussé. Merci vécu après le "
        "coussin. Fin : l'éclat du début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le train de coussins de Sarah (noyau dump). Relance : "
        "Que font Sarah et Victorino ?\n"
        "- Lieu du dump (salon puis porte du jardin, vapeur, cuillère, "
        "thym, canapé, coussins). Papa ajouté. Strip « tout chaud » / "
        "« encore ».\n"
        "- Ouverture inventée (vapeur qui colle à la vitre), pas un "
        "gabarit v2, pas « Sarah joue au salon ».\n"
        "- Indice unique : éclat de coussin. BAN figue, robinet, planche, "
        "cerceau, émail, samare, bassine. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout chaud » du dump.\n"
        "- Leçon non dite : on la voit quand le tirage seul échoue, puis "
        "quand il soulève et elle tire. Pas « vous jouez ensemble ». "
        "Pas « tailles différentes ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Sarah invite Victorino. Que "
        "font-ils ? ». expected jouer ensemble. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 100 / 032 / 064 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_col_pol_001_05.py` (Sarah).\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Confirm plus vif vers le coussin.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
