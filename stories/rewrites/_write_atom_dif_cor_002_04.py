#!/usr/bin/env python3
"""ATOM-DIF.COR.002-04 — Les fraises de Nina (F-NAR-019, N3, DIF.COR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.002-04"
TITLE = "Les fraises de Nina"
N3 = LIMITS["N3"]
CHARS = "Nina, Victorino, papa, maman"
SETTING = "jardin des fraisiers puis cuisine"
INDICE = "éclat de fraisier"
FIL = (
    "Une goutte tient sous une feuille. Terre noire, escargot, arrosoir "
    "vide. Sur la tige, un éclat de fraisier brille. Nina veut une tarte, "
    "maintenant. Elle saisit trop vite : les fraises tombent. Victorino "
    "arrive, chemise qui remonte. Un rire commence. Elle ferme la bouche, "
    "attend, ils cueillent. Le rouleau manque. Elle refuse de foncer. "
    "Merci vécu. La pâte colle à la chemise. Elle refuse. L'éclat de "
    "fraisier tient sur la feuille."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tiroir|cuivre|buis|émail|email|écorce|ecorce|samare|bassine|"
    r"enveloppe|dalle|dalles|plaque|pierre|pierres)\b",
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
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai attendu",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "tu attends ton tour",
    "tu as attendu",
    "c'est ton tour",
    "tailles différentes",
    "tailles differentes",
    "plus rond",
    "plus mince",
    "vous jouez ensemble",
    "on peut jouer ensemble",
    "on a joué ensemble",
    "vous jouez",
    "on joue",
    "il ne faut pas rire",
    "l'amitié ne dépend",
    "l'amitie ne depend",
    "grain de",
    "grains",
    "lune d'étain",
    "lune d'etain",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "bol de fraises",
    "bol émaillé",
    "bol emaille",
    "cerisier",
    "plaid",
    "éclat de fraise",
    "éclat d'émail",
    "éclat d'email",
    "éclat de tiroir",
    "éclat de cuivre",
    "éclat de buis",
    "éclat d'écorce",
    "éclat de écorce",
    "éclat d'ecorce",
    "éclat de cerceau",
    "éclat de pince",
    "éclat de samare",
    "éclat de bassine",
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "éclat de dalle",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
    "éclat de casserole",
    "éclat de nappe",
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
    "éclat de farine",
    "éclat de grille",
    "éclat de pli",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de carreau",
    "éclat de orange",
    "éclat de lampe",
    "éclat de citron",
    "éclat de quille",
    "éclat de pin",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de tapis",
    "éclat de corbeille",
    "éclat de croissant",
    "éclat de poire",
    "éclat de sac",
    "éclat de cloche",
    "éclat de volet",
    "éclat de bâche",
    "éclat de bache",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de poisson",
    "éclat de mie",
    "éclat de page",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de couloir",
    "éclat de cour",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de fraisier",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_tarte_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="corps",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_ferme_la_bouche_ils_cueillent; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="rouleau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_trouve_le_rouleau; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de fraisier",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de fraisier",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_feuille; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": (
        "jouer | on joue | pas une blague | pas blague | cueillir | la tarte"
    ),
    "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    "engine_ok_text": "Oui, on joue.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin,fraisiers",
        [
            "narrateur|Une goutte tient sous une feuille.",
            "narrateur|La terre est fraîche, un peu noire.",
            "narrateur|Un escargot avance sur une barquette.",
            "narrateur|L'arrosoir est couché, vide.",
            "narrateur|Ça sent le vert et le sucre.",
            "papa|Tu as vu la goutte, Nina ?",
            "enfant-f|Elle brille.",
            "papa|Elle tient à la feuille ?",
            "enfant-f|Oui, papa.",
            "maman|Le jardin sent le sucre, là.",
            "enfant-f|Oui, maman.",
            "narrateur|Nina lève la feuille du fraisier.",
            "narrateur|La feuille est rêche, un peu poussiéreuse.",
            "narrateur|La goutte glisse dans la terre.",
            "enfant-f|Elle est partie.",
            "narrateur|Une petite bête se cache, puis part.",
            "narrateur|Sur la tige, un éclat de fraisier brille.",
            "enfant-f|Il brille, maman !",
            "maman|Tu le vois, sur la tige ?",
            "enfant-f|Oui, il brille.",
            "enfant-f|Je veux une tarte, maintenant !",
            "papa|Avec des fraises ?",
            "enfant-f|Beaucoup, papa.",
            "maman|On en cueille d'abord ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina saisit trop de fraises d'un coup.",
            "narrateur|Les fruits glissent entre ses doigts.",
            "narrateur|Ils tombent dans la terre noire.",
            "enfant-f|Elles sont par terre !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu, lourdes.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu veux la tarte avec Victorino ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont dans les feuilles ?",
            "enfant-f|Oui, maman.",
            "narrateur|En ce moment, Victorino arrive entre les rangs.",
            "narrateur|Il a les mains un peu rouges.",
            "enfant-f|Tu viens ?",
            "narrateur|Il se penche vers un fraisier bas.",
            "narrateur|Sa chemise remonte un peu.",
            "narrateur|Nina ouvre la bouche.",
            "narrateur|Un petit rire commence.",
            "enfant-f|Oh.",
            "narrateur|Nina ferme la bouche.",
            "narrateur|Elle regarde la barquette.",
            "enfant-f|On cueille pour la tarte.",
            "narrateur|Victorino ne dit rien, d'abord.",
            "narrateur|Il regarde les fraisiers, puis Nina.",
            "copain|Oui.",
            "narrateur|Nina veut passer entre deux rangs.",
            "narrateur|Victorino ne passe pas, trop juste.",
            "copain|Attends.",
            "narrateur|Nina reste.",
            "narrateur|Elle n'avance pas.",
            "narrateur|Victorino contourne le rang, sans se presser.",
            "papa|Vous cueillez, tous les deux ?",
            "enfant-f|Oui, papa.",
            "copain|Moi, le fraisier du fond.",
            "narrateur|Ils posent les fraises dans la barquette.",
            "narrateur|Le bois de la barquette est rêche.",
            "narrateur|Une feuille colle au poignet de Nina.",
            "enfant-f|Elle pique.",
            "papa|C'est la feuille ?",
            "enfant-f|Oui.",
            "enfant-f|Il en faut d'autres.",
            "maman|Le fraisier du fond en a.",
            "narrateur|L'éclat de fraisier tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le corps n'est pas une blague.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "robinet,pate",
        [
            "narrateur|Au robinet, l'eau est froide.",
            "narrateur|Les fraises deviennent plus brillantes.",
            "narrateur|Une goutte mouille la chemise de Victorino.",
            "copain|Elle est froide.",
            "enfant-f|L'eau pique les mains.",
            "narrateur|Ils rient de l'eau.",
            "papa|Elle est froide, cette goutte ?",
            "enfant-f|Oui, papa.",
            "maman|On rentre pour la pâte ?",
            "enfant-f|Oui, maman.",
            "narrateur|Dans la cuisine, la pâte attend.",
            "narrateur|Elle est molle et un peu collante.",
            "enfant-f|On l'étale, maintenant !",
            "copain|Moi le rouleau.",
            "narrateur|Le rouleau n'est pas sur la table.",
            "enfant-f|Il manque !",
            "narrateur|Nina étale avec les mains, trop vite.",
            "narrateur|La pâte se déchire d'un côté.",
            "enfant-f|Elle est trouée.",
            "narrateur|Le sourire de Nina ne revient pas.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Elle regarde la barquette.",
            "narrateur|Une feuille de fraisier est restée dessus.",
            "narrateur|Sur la tige, l'éclat de fraisier brille.",
            "enfant-f|Le rouleau, papa ?",
            "papa|Tu le cherches où ?",
            "enfant-f|Près de l'eau.",
            "narrateur|Le rouleau attend près de l'évier.",
            "narrateur|Nina l'apporte, sans se presser.",
            "narrateur|Victorino tient un bout de pâte.",
            "narrateur|Nina tient l'autre bout.",
            "narrateur|La pâte devient un tapis.",
            "enfant-f|Tu tiens ce bord ?",
            "narrateur|Victorino ne dit rien.",
            "narrateur|Il pose une main sur la pâte, sans parler.",
            "copain|Oui.",
            "narrateur|Nina pose les fraises, une par une.",
            "narrateur|Elles font un petit cercle rouge.",
            "narrateur|Le milieu reste vide.",
            "enfant-f|Il manque le centre.",
            "copain|J'en ai une.",
            "narrateur|Victorino pose la dernière fraise au milieu.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux mains sur la pâte.",
            "maman|Victorino, tu as vu le cercle ?",
            "copain|Oui.",
            "papa|Un autre tour de rouleau ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le ventre de Nina se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "four,tarte",
        [
            "narrateur|Nina veut la tarte au chaud, d'un coup.",
            "narrateur|Elle pousse le moule trop vite.",
            "narrateur|La pâte glisse d'un bord.",
            "enfant-f|Ça tombe !",
            "copain|Attends.",
            "narrateur|De la pâte colle à la chemise de Victorino.",
            "narrateur|Nina ouvre la bouche.",
            "narrateur|Un petit rire revient, presque.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape fort, dans sa poitrine.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Elle regarde la feuille, sur la table.",
            "narrateur|L'éclat de fraisier revient, sur la feuille.",
            "enfant-f|L'éclat, papa ?",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur la feuille.",
            "maman|La tarte, Nina ?",
            "enfant-f|Oui.",
            "narrateur|Nina attend que la pâte tienne.",
            "narrateur|Victorino tient le bord, sans parler.",
            "narrateur|Ils poussent le moule, sans se presser.",
            "narrateur|La porte du four fait un petit clac.",
            "enfant-f|C'est passé.",
            "copain|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "tarte",
        [
            "narrateur|Ils attendent près de la fenêtre.",
            "narrateur|Dehors, l'escargot a avancé.",
            "enfant-f|Il va loin, papa.",
            "papa|Tu le vois sur le bois ?",
            "enfant-f|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|La tarte sort.",
            "narrateur|Ça sent le sucre chaud.",
            "narrateur|Le bord est un peu doré.",
            "enfant-f|On goûte le bord ?",
            "maman|Vous soufflez un peu ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina souffle.",
            "narrateur|Victorino souffle aussi.",
            "copain|C'est doux.",
            "enfant-f|La tarte est là.",
            "maman|Elle est là, Nina.",
            "enfant-f|Oui, maman.",
            "narrateur|Nina pose la joue près de la feuille.",
            "narrateur|La feuille est tiède, un peu.",
            "enfant-f|L'éclat est là, papa.",
            "papa|Tu le vois sur la feuille ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'éclat de fraisier tient sur la feuille.",
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
            if re.search(rf"(?<!\w){re.escape(bad)}(?!\w)", low):
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if blob.count("le corps n'est pas une blague") != 1:
        raise SystemExit(f"{SID}: leçon dite hors question")
    for bad in (
        "éclat de fraise",
        "éclat d'émail",
        "éclat de tiroir",
        "éclat de cuivre",
        "éclat de buis",
        "tiroir",
        "cuivre",
        "buis",
        "émail",
        "écorce",
        "plus rond",
        "plus mince",
        "bol de fraises",
        "cerisier",
        "plaid",
    ):
        if bad in blob:
            raise SystemExit(f"{SID}: ban {bad}")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Le corps n'est pas une blague. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
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
        "- **Public :** N3 (≤16), audio familial\n"
        "- **Leçon :** DIF.COR.002 — le corps n'est pas une blague ; on "
        "joue (vécue : chemise qui remonte ; un rire commence ; Nina "
        "ferme la bouche ; Attends ; elle contourne avec lui ; pâte sur "
        "la chemise ; rire presque ; elle refuse de foncer ; deux mains "
        "sur la pâte)\n"
        "- **Personnages :** Nina, Victorino, papa, maman. Troupe D16. "
        "Victorino = copain (rythme lent, « Attends », silence). Papa et "
        "maman parlent. Maman ajoutée.\n"
        "- **Lieu :** jardin des fraisiers puis cuisine. Goutte sous "
        "feuille, terre, escargot, arrosoir vide, barquette, robinet, "
        "pâte, rouleau, four. Distinct COR.001-01 (pas bol de fraises, "
        "pas éclat d'émail).\n"
        "- **Indice unique :** éclat de fraisier (brille sous la feuille "
        "→ tremble → brille au silence → revient sur la feuille → tient "
        "sur la feuille). Pas éclat de fraise.\n"
        "- **Question moteur :** Le corps n'est pas une blague. Que "
        "fait-on ? → jouer.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte tient sous une feuille. Terre noire, escargot sur la "
        "barquette, arrosoir vide. Nina lève la feuille. Sur la tige, un "
        "éclat de fraisier brille. Elle veut une tarte **maintenant**. "
        "Première idée : saisir trop de fraises. Elles tombent. Sourire "
        "parti, épaules basses. Papa s'accroupit. Victorino arrive. Sa "
        "chemise remonte. Un rire commence. Elle ferme la bouche, "
        "regarde la barquette. Il se tait, puis oui. Entre les rangs, "
        "trop juste : Attends. Elle reste. Il contourne. Ils cueillent. "
        "Question. Au robinet, l'eau mouille la chemise : ils rient de "
        "l'eau. En cuisine, le rouleau manque. Elle étale trop vite : la "
        "pâte se déchire. Elle refuse de foncer, écoute, retrouve "
        "l'éclat, trouve le rouleau. Deux mains sur la pâte. Merci vécu. "
        "Elle pousse le moule trop vite : pâte sur la chemise, rire "
        "presque. Elle refuse. L'éclat de fraisier tient sur la feuille.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin des fraisiers, goutte sous feuille, terre "
        "noire, escargot, arrosoir vide, sucre vert, puis cuisine.\n"
        "- Désir : une tarte aux fraises, maintenant.\n"
        "- Objet : barquette, fraisiers, pâte, rouleau, moule, four.\n"
        "- Indice unique : éclat de fraisier, vu dès l'ouverture, payé "
        "à la fin.\n"
        "- Urgence douce : la tarte, maintenant ; Victorino vient "
        "d'arriver.\n"
        "- Imprévu 1 : elle saisit trop vite ; les fraises tombent ; le "
        "rouleau manque ; la pâte se déchire.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : moule trop vite ; pâte sur la chemise ; "
        "rire presque ; Attends.\n"
        "- Résolution : elle ferme la bouche, refuse de foncer, deux "
        "mains sur la pâte, dernière fraise au centre.\n"
        "- Retour : fenêtre, escargot du début, tarte dorée, éclat sur "
        "la feuille.\n\n"
        "## Vécu\n\n"
        "Nina propose, veut **maintenant**. Victorino prend son temps, "
        "pose une limite, se tait. Le silence compte. Papa s'accroupit, "
        "ne récite pas « le corps n'est pas une blague ». La leçon se "
        "voit : la bouche qui se ferme, l'eau dont on rit, les deux "
        "mains, le rire qui n'arrive pas. Merci vécu après les deux "
        "mains sur la pâte. Fin : l'éclat du début tient sur la feuille.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : jardin des fraisiers "
        "puis cuisine, goutte, terre, escargot. Pas bol de fraises, pas "
        "éclat d'émail / tiroir / cuivre / buis / écorce / éclat de "
        "fraise.\n"
        "- Ouverture inventée (goutte sous feuille, escargot, arrosoir "
        "vide), pas un gabarit v2. example4 004 / 036 / 068 : corps "
        "(sourire parti, poitrine, accroupi), 2e ruse, refuse de foncer.\n"
        "- Indice unique : éclat de fraisier. Pas merle-trois-notes, "
        "miel, tache / flèche / marque / symbole.\n"
        "- Tics encore / déjà / tout doux / tout calme et `aujourd'hui,` "
        "retirés. Morale « le corps n'est pas une blague » hors question "
        "retirée. Maman ajoutée.\n"
        "- Question moteur inchangée. 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 5 × éclat de fraisier\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
