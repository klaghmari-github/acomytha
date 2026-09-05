#!/usr/bin/env python3
"""ATOM-DIF.COR.001-04 — Le tunnel du drap (F-NAR-019, N3, DIF.COR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-04"
TITLE = "Le tunnel du drap"
N3 = LIMITS["N3"]
CHARS = "Nina, Aniss, papa, maman"
SETTING = "cour, fil à linge, cerceau rouge, drap au soleil"
INDICE = "éclat de cerceau"
FIL = (
    "Le fil à linge fait tic dans la cour. Une feuille colle au cerceau "
    "rouge. Sur le fer, un éclat de cerceau brille. Nina veut un tunnel "
    "pour la voiture, maintenant. Elle saisit trop vite : le cerceau "
    "roule. Aniss arrive. Elle invite, il attend, ils tiennent le fer. "
    "Le drap glisse. Elle refuse de foncer. Merci vécu. L'éclat de "
    "cerceau tient sur le fer."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(émail|email|samare|bassine|enveloppe|dalle|dalles|plaque|"
    r"pierre|pierres|émail|email)\b",
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
    "vous jouez ensemble",
    "on peut jouer ensemble",
    "on a joué ensemble",
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
    "éclat de pince",
    "éclat d'émail",
    "éclat d'email",
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
        emphasis="éclat de cerceau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_tunnel_avec_aniss_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Aniss",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=nina_invite_ils_tiennent_le_fer_ensemble; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="drap",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_aniss_tient_le_drap; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de cerceau",
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
        emphasis="éclat de cerceau",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_fer; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer ensemble",
    "accepted_examples": (
        "jouer ensemble | ensemble | ils jouent | on joue | jouer"
    ),
    "retry_prompt": "Ils jouent. Que font Nina et Aniss ?",
    "engine_ok_text": "Oui, ils jouent ensemble.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Le fil à linge fait tic, dans la cour.",
            "narrateur|Le tic est sec, un peu vif.",
            "narrateur|La chaleur pique les pieds nus.",
            "narrateur|Un drap blanc pend au soleil.",
            "narrateur|Le tissu est chaud, un peu rêche.",
            "enfant-f|Il sent le soleil, papa.",
            "papa|Tu as mis la main dessus ?",
            "enfant-f|Oui, papa.",
            "enfant-f|C'est chaud.",
            "maman|Le drap a séché sur le fil.",
            "narrateur|Une feuille sèche colle au cerceau rouge.",
            "narrateur|Le cerceau rouge attend contre le mur.",
            "narrateur|Nina lève la feuille du fer.",
            "narrateur|Sur le fer, un éclat de cerceau brille.",
            "enfant-f|Il brille, maman !",
            "maman|Tu le vois, sur le fer ?",
            "enfant-f|Oui, il brille.",
            "narrateur|Une petite voiture de bois attend à l'ombre.",
            "narrateur|Ses roues sont un peu poussiéreuses.",
            "enfant-f|Je veux un tunnel, maintenant !",
            "papa|Pour la voiture ?",
            "enfant-f|Oui, avec le cerceau.",
            "maman|Avec le drap aussi ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina saisit le cerceau trop vite.",
            "narrateur|Le fer glisse entre ses doigts.",
            "narrateur|Le cerceau roule dans les feuilles sèches.",
            "enfant-f|Il est parti !",
            "narrateur|L'éclat de cerceau tremble, puis tient.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu, lourdes.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu veux le tunnel avec Aniss ?",
            "enfant-f|Oui, papa.",
            "maman|Tes pieds sont dans l'herbe ?",
            "enfant-f|Oui, maman.",
            "narrateur|En ce moment, Aniss arrive près du fil.",
            "narrateur|Il a les genoux un peu verts.",
            "enfant-f|Tu viens ?",
            "enfant-f|On fait un tunnel.",
            "narrateur|Aniss ne dit rien, d'abord.",
            "narrateur|Il regarde le cerceau, puis Nina.",
            "copain|Oui.",
            "narrateur|Nina veut tenir le cerceau bien haut.",
            "narrateur|Aniss tend les mains, trop bas.",
            "narrateur|Les doigts d'Aniss glissent sur le fer.",
            "enfant-f|Le haut est loin.",
            "copain|Attends.",
            "narrateur|Nina baisse un peu les bras.",
            "narrateur|Aniss tient le bas du cerceau.",
            "narrateur|Nina tient le haut, moins loin.",
            "papa|Vous tenez le fer ?",
            "enfant-f|Oui, papa.",
            "copain|Moi, le bas.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina invite Aniss.",
            "narrateur|Que font-ils ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "drap,voiture",
        [
            "narrateur|Le drap tombe sur le cerceau.",
            "narrateur|Ça fait une petite grotte claire.",
            "narrateur|La lumière passe à travers le tissu.",
            "enfant-f|C'est blanc, dedans.",
            "papa|Oui.",
            "narrateur|Nina pousse la voiture trop vite.",
            "narrateur|Le drap glisse d'un côté.",
            "narrateur|Les roues s'arrêtent dans le tissu.",
            "enfant-f|Elle ne passe pas.",
            "narrateur|Le sourire de Nina ne revient pas.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Elle pose les mains sur le drap.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Elle regarde le cerceau, elle écoute la cour.",
            "narrateur|Le fil à linge fait tic, sec.",
            "narrateur|Sur le fer, l'éclat de cerceau brille.",
            "enfant-f|Tu tiens ce coin ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il pose une main sur le drap, sans parler.",
            "copain|Oui.",
            "narrateur|Nina attend que la grotte tienne.",
            "narrateur|Elle pousse la voiture, sans se presser.",
            "narrateur|Les roues font un bruit de bois.",
            "copain|Elle arrive !",
            "enfant-f|Elle est passée.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux mains sur le drap.",
            "maman|Aniss, tu as vu la voiture ?",
            "copain|Oui.",
            "papa|Un autre tour ?",
            "enfant-f|Oui, papa.",
            "narrateur|Aniss pousse, à son tour.",
            "narrateur|Nina attend de l'autre côté.",
            "narrateur|La voiture ressort, un peu chaude.",
            "narrateur|Une feuille sèche est restée dessus.",
            "papa|Elle vient du platane, ça ?",
            "enfant-f|Oui.",
            "narrateur|Le ventre de Nina se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "cerceau,feuilles",
        [
            "narrateur|Nina veut le cerceau plus haut, d'un coup.",
            "narrateur|Elle lève le fer trop vite.",
            "narrateur|Aniss n'atteint plus le bas.",
            "copain|Attends.",
            "enfant-f|Je le tiens !",
            "narrateur|Le cerceau penche vers l'herbe.",
            "narrateur|Le drap glisse, presque.",
            "enfant-f|Ça tombe !",
            "narrateur|Nina veut rattraper le fer, d'un coup.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape fort, dans sa poitrine.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Elle regarde le cerceau.",
            "narrateur|Elle écoute le tic du fil.",
            "narrateur|Le fer est tiède sous les doigts.",
            "enfant-f|L'éclat, papa ?",
            "papa|Tu le vois, toi ?",
            "enfant-f|Non, plus sur le fer.",
            "narrateur|Nina baisse le cerceau, sans se presser.",
            "narrateur|Aniss reprend le bas.",
            "enfant-f|Il est là.",
            "papa|Sur ce fer ?",
            "enfant-f|Oui, sur ce fer.",
            "narrateur|L'éclat de cerceau revient, sur le fer.",
            "maman|La voiture, Nina ?",
            "enfant-f|Oui.",
            "narrateur|Ils tiennent le drap, l'un et l'autre.",
            "narrateur|La voiture traverse la grotte claire.",
            "enfant-f|C'est passé.",
            "copain|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "drap",
        [
            "narrateur|Le cerceau rouge repose contre le mur.",
            "narrateur|Une feuille sèche reste collée au fer.",
            "enfant-f|L'éclat est là, papa.",
            "papa|Tu le vois sur le fer ?",
            "enfant-f|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|Le drap sent le soleil.",
            "narrateur|Le tissu est chaud, un peu rêche.",
            "enfant-f|La voiture a traversé.",
            "maman|Elle a traversé, Nina.",
            "enfant-f|Oui, maman.",
            "narrateur|Nina pose la joue près du drap.",
            "narrateur|Le drap est tiède, un peu.",
            "enfant-f|C'est chaud.",
            "narrateur|Aniss pose la voiture à l'ombre.",
            "narrateur|Les roues ont une trace d'herbe.",
            "narrateur|L'éclat de cerceau tient sur le fer.",
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
    for bad in (
        "éclat de pince",
        "émail",
        "samare",
        "bassine",
        "enveloppe",
        "dalle",
        "plaque",
        "pierre",
    ):
        if bad in blob:
            raise SystemExit(f"{SID}: ban {bad}")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Nina invite Aniss. Que font-ils ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer ensemble":
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
        "- **Leçon :** DIF.COR.001 — jouer ensemble (vécue : Nina veut le "
        "tunnel maintenant ; saisit trop vite ; invite Aniss ; il attend, "
        "tient le bas ; le drap glisse ; elle refuse de foncer ; deux "
        "mains sur le drap ; la voiture passe)\n"
        "- **Personnages :** Nina, Aniss, papa, maman. Troupe D16. Aniss "
        "= copain (rythme lent, « Attends », silence). Papa et maman "
        "parlent.\n"
        "- **Lieu :** cour, fil à linge, cerceau rouge, drap au soleil. "
        "Voiture de bois, feuilles sèches, platane. Pas éclat de pince.\n"
        "- **Indice unique :** éclat de cerceau (brille sous la feuille → "
        "tremble → brille au silence → revient après le fer trop haut → "
        "tient sur le fer).\n"
        "- **Question moteur :** Nina invite Aniss. Que font-ils ? → "
        "jouer ensemble.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le fil à linge fait tic dans la cour. La chaleur pique les pieds. "
        "Un drap blanc pend au soleil. Une feuille colle au cerceau rouge. "
        "Sur le fer, un éclat de cerceau brille. Nina veut un tunnel pour "
        "la voiture **maintenant**. Première idée : saisir le cerceau d'un "
        "coup. Il roule dans les feuilles. Sourire parti, épaules basses. "
        "Papa s'accroupit. Aniss arrive. Elle invite. Il se tait, puis "
        "oui. Elle tient trop haut : ses doigts glissent. Il dit Attends. "
        "Ils tiennent le fer, haut et bas. Question. Le drap fait grotte. "
        "Elle pousse trop vite : le drap glisse. Elle refuse de foncer, "
        "écoute le tic, retrouve l'éclat. Aniss pose une main, sans "
        "parler. La voiture passe. Merci vécu. Elle lève trop haut : "
        "l'éclat manque. Elle refuse, baisse le fer. L'éclat de cerceau "
        "tient sur le fer.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cour, fil à linge qui tique, chaleur, drap au soleil, "
        "feuille sur le cerceau rouge, voiture à l'ombre, platane.\n"
        "- Désir : un tunnel pour la voiture, avec Aniss, maintenant.\n"
        "- Objet : cerceau rouge, drap, voiture de bois, fil à linge.\n"
        "- Indice unique : éclat de cerceau, vu dès l'ouverture, payé à "
        "la fin.\n"
        "- Urgence douce : le drap est chaud, Aniss vient d'arriver.\n"
        "- Imprévu 1 : elle saisit trop vite ; le cerceau roule ; trop "
        "haut, les doigts d'Aniss glissent.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : lever le fer trop haut ; le drap "
        "glisse ; l'éclat manque ; Aniss dit Attends.\n"
        "- Résolution : elle refuse de foncer, baisse le cerceau, Aniss "
        "tient le bas, deux mains sur le drap.\n"
        "- Retour : cerceau contre le mur, feuille collée, éclat du "
        "début, drap qui sent le soleil.\n\n"
        "## Vécu\n\n"
        "Nina propose, veut **maintenant**. Aniss prend son temps, pose "
        "une limite, se tait. Le silence compte. Papa s'accroupit, ne "
        "récite pas « jouer ensemble ». La leçon se voit : deux hauteurs, "
        "deux mains, la voiture qui passe. Merci vécu après les deux "
        "mains sur le drap. Fin : l'éclat du début tient sur le fer.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : cour, fil à linge, "
        "cerceau rouge, drap au soleil. Pas éclat de pince, pas émail / "
        "samare / bassine / enveloppe / dalle / plaque / pierre.\n"
        "- Ouverture inventée (tic du fil, feuille collée), pas un "
        "gabarit v2. example4 096 / 028 / 060 : corps (sourire parti, "
        "poitrine, accroupi), 2e ruse, refuse de foncer.\n"
        "- Indice unique : éclat de cerceau. Pas merle-trois-notes, miel, "
        "tache / flèche / marque / symbole.\n"
        "- Tics encore / déjà / tout doux / tout calme et `aujourd'hui,` "
        "retirés. Morale « vous jouez ensemble » retirée.\n"
        "- Question moteur inchangée. 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 5 × éclat de cerceau\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
