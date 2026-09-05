#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-01 — Nina et le gâteau au citron (F-NAR-019, N2, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-01"
TITLE = "Nina et le gâteau au citron"
N2 = LIMITS["N2"]
CHARS = "Nina, papa, maman"
SETTING = (
    "marché, pavés, cagette, citron, gâteau, poire, "
    "sac, plateau, miettes, bois"
)
INDICE = "éclat de cagette"
FIL = (
    "Un citron échappe aux doigts de maman. Sur le bois, "
    "un éclat de cagette luit. Nina veut le gâteau au citron, "
    "maintenant. Le plateau est vide. Sourire parti. Trou dans "
    "la poitrine. Papa s'accroupit. Nina dit qu'elle est déçue. "
    "Merci vécu. Deuxième ruse : poire trop haute, presque prise, "
    "autre enfant. Elle refuse de foncer. Elle choisit une poire "
    "plus basse. Un éclat de cagette tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|gomme|berge|"
    r"brouette|couverture|capuche|paillasson|fauteuil|coffre|"
    r"haie|housse|cageot|étal|etal|caisse|maîtresse|maitresse|"
    r"grand-père|grand-pere|jardinier|bibliothécaire|bibliothecaire|"
    r"gardienne|sami)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "j'ai dit",
    "j ai dit",
    "tu as nommé",
    "tu as nomme",
    "c'est de la déception",
    "c est de la deception",
    "c'est de la deception",
    "c'est de la joie",
    "c est de la joie",
    "on peut chercher une autre idée",
    "on peut chercher une autre idee",
    "c'est une autre idée",
    "c est une autre idee",
    "une autre idée peut venir",
    "une autre idee peut venir",
    "un souhait peut attendre",
    "ce n'est pas honteux",
    "ce n est pas honteux",
    "être déçu",
    "etre decu",
    "être déçue",
    "etre decue",
    "tu as trouvé une autre idée",
    "tu as trouve une autre idee",
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
    "il ne faut pas rire",
    "on ne rit pas",
    "bravo. tu as",
    "tu as dit : je suis",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de citron",
    "éclat d'étal",
    "éclat d'etal",
    "éclat de caisse",
    "éclat de cageot",
    "éclat de poire",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de couverture",
    "éclat de capuche",
    "éclat de paillasson",
    "éclat de fauteuil",
    "éclat de coffre",
    "éclat de haie",
    "éclat de housse",
    "éclat de plateau",
    "éclat de sac",
    "éclat de pavé",
    "éclat de pave",
    "toute calme",
    "tout calme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cagette",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_gateau_maintenant; "
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
            "sous_texte=le_gateau_n_est_plus_la_que_dit_nina; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="poire",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_dit_une_poire_sans_slogan; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de cagette",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=poire_presque_prise_trop_haute_autre_enfant; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cagette",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçu",
    "accepted_examples": (
        "déçu | je suis déçu | autre idée | une poire | une autre idée"
    ),
    "retry_prompt": "Nina cherche une autre idée. Que dit-elle d'abord ?",
    "engine_ok_text": "Oui, déçu.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "marché,citron",
        [
            "narrateur|Un citron échappe aux doigts de maman.",
            "enfant-f|Il roule, papa !",
            "papa|Tu le rattrapes, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina pose le pied devant le fruit jaune.",
            "enfant-f|Je l'ai, maman.",
            "maman|Il est froid, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le citron sent fort, près du sac.",
            "enfant-f|Ça sent le citron.",
            "papa|Tu le sens, toi ?",
            "enfant-f|Oui, papa.",
            "narrateur|Maman ouvre une cagette de bois, près des pavés.",
            "enfant-f|Elle est en bois.",
            "maman|Tu la vois, la cagette ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur le bois, un éclat de cagette luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Nina pose le citron dans la cagette.",
            "enfant-f|Il tient.",
            "maman|Il est rentré ?",
            "enfant-f|Oui, maman.",
            "narrateur|Les pavés du marché sont froids sous les chaussures.",
            "enfant-f|Ils sont froids.",
            "papa|Tes pieds sont bien, Nina ?",
            "enfant-f|Un peu froids.",
            "narrateur|Le sac de papa tape contre sa jambe.",
            "enfant-f|Le sac est lourd.",
            "maman|Je tiens le sac, Nina.",
            "enfant-f|D'accord, maman.",
            "narrateur|Un plateau de gâteaux attend, un peu plus loin.",
            "enfant-f|Des gâteaux !",
            "papa|Tu les vois, les jaunes ?",
            "enfant-f|Le gâteau au citron.",
            "narrateur|En ce moment, Nina tend les deux mains.",
            "enfant-f|Je veux le gâteau, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina avance trop vite vers le plateau.",
            "narrateur|Ses doigts touchent seulement des miettes.",
            "narrateur|Le plateau est vide, près des citrons.",
            "enfant-f|Il n'y en a plus.",
            "maman|Le gâteau est parti, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Ça sent le citron, même sans gâteau.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie du gâteau fait un trou.",
            "narrateur|L'envie et le trou se bousculent sans place.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-f|J'ai mal au ventre.",
            "papa|Ta gorge est serrée, Nina ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Papa s'accroupit à la même hauteur, sans parler.",
            "maman|Tes mains sont chaudes, Nina ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|Je suis déçue.",
            "narrateur|L'éclat de cagette tremble, puis tient.",
            "narrateur|Nina lève les yeux vers les fruits jaunes.",
            "enfant-f|Des citrons.",
            "papa|Tu les vois, Nina ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le gâteau n'est plus là.",
            "narrateur|Que dit Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "marché",
        [
            "narrateur|Nina reste près de la cagette, un moment.",
            "enfant-f|Le gâteau, maintenant.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Je le prends.",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Nina refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe les fruits, un instant.",
            "narrateur|Elle écoute le marché, près des pavés.",
            "papa|Tu restes un peu, Nina ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Nina.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le citron est froid, sous les doigts.",
            "enfant-f|Il est lisse.",
            "narrateur|La poitrine de Nina ralentit un peu.",
            "narrateur|Les épaules se relèvent un peu.",
            "enfant-f|Une poire, alors.",
            "maman|Tu la vois, la poire ?",
            "enfant-f|Oui, maman.",
            "papa|Elle est jaune, Nina ?",
            "enfant-f|Un peu verte.",
            "narrateur|Nina tend le doigt vers une poire.",
            "enfant-f|Celle-là.",
            "maman|Tes joues sont chaudes, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Nina se desserre.",
            "papa|On s'approche sans se presser ?",
            "enfant-f|Oui.",
            "narrateur|Ils se lèvent, sans se bousculer.",
            "enfant-f|La poire, papa.",
            "papa|On y va, sans se presser.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "marché,poire",
        [
            "narrateur|Nina lève la main vers la poire.",
            "enfant-f|Je la prends !",
            "narrateur|Un enfant plus grand tend la main vers la poire.",
            "narrateur|La poire bascule au bord, trop haute.",
            "enfant-f|Elle part !",
            "narrateur|La poire est presque prise, au-dessus des doigts.",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la poire, un instant.",
            "narrateur|Elle écoute le marché, près de la cagette.",
            "narrateur|Sur le bois, un éclat de cagette luit.",
            "enfant-f|Là, sur le bois.",
            "papa|Tu vois le point, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'enfant plus grand prend la poire trop haute.",
            "enfant-f|Pas celle-là.",
            "maman|Tu en vois une autre, Nina ?",
            "enfant-f|Plus bas.",
            "narrateur|Une poire plus basse attend à hauteur de main.",
            "enfant-f|Celle-là, maman.",
            "papa|Tu la prends, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina détache la poire plus basse, sans se presser.",
            "narrateur|La peau est lisse et froide.",
            "enfant-f|Elle est lourde.",
            "maman|Elle tient dans ta main ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina la serre contre elle.",
            "enfant-f|Ma poire.",
            "papa|Elle a une petite trace, Nina.",
            "enfant-f|Elle a failli partir.",
            "narrateur|La poire sent le sucre, un peu.",
            "enfant-f|Et le citron, autour.",
            "papa|On reste près de la cagette ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la cagette.",
            "narrateur|Maman essuie un peu de jus sur le bois.",
            "enfant-f|La poire a une trace, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, près du bord.",
            "maman|On est bien, ici.",
            "narrateur|Nina tapote le bois de la cagette.",
            "enfant-f|Il a une trace de jus.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|La poire est restée, Nina.",
            "enfant-f|Oui, avec nous.",
            "narrateur|Ça sent le citron, un peu tiède.",
            "enfant-f|Et le bois, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le marché sent le sucre, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|La poire reste contre le sac.",
            "narrateur|Un éclat de cagette tient sur le bois.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-f"):
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
        for key in ("expected_answer", "accepted_examples", "retry_prompt"):
            if cid != "CHK_T0000_P0000_Q0001":
                by[cid][key] = None
                if by[cid].get(key) is not None:
                    raise SystemExit(f"{cid}: {key} devait rester null")
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
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque accroupit")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut chercher une autre idée",
        "c'est de la déception",
        "c est de la deception",
        "c'est une autre idée",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "l'histoire est finie",
        "un souhait peut attendre",
        "ce n'est pas honteux",
        "être déçu",
        "etre decu",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le gâteau n'est plus là. Que dit Nina ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçu":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "déçu | je suis déçu | autre idée | une poire | une autre idée"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Nina cherche une autre idée. Que dit-elle d'abord ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: expected hors Q")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: accepted hors Q")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: retry hors Q")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis déçue" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_decue = blob.count("je suis déçue")
    if n_decue != 1:
        raise SystemExit(f"{SID}: je suis déçue ×{n_decue}")
    if "une poire" not in by["CHK_T0000_P0000_C0001"]["text"].lower():
        raise SystemExit(f"{SID}: poire absente après la question")
    if "gâteau" not in blob and "gateau" not in blob:
        raise SystemExit(f"{SID}: manque gâteau")
    if "citron" not in blob:
        raise SystemExit(f"{SID}: manque citron")
    if "poire" not in blob:
        raise SystemExit(f"{SID}: manque poire")
    if "marché" not in blob and "marche" not in blob:
        raise SystemExit(f"{SID}: manque marché")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    if "trou" not in opening:
        raise SystemExit(f"{SID}: manque trou dans la poitrine")
    end_txt = by["CHK_T0000_P0000_END"]["text"].lower()
    if "trop haute" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (trop haute)")
    if "presque prise" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (presque prise)")
    if "enfant plus grand" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (autre enfant)")
    if "papa" not in by["CHK_T0000_P0000_END"]["script"].lower():
        raise SystemExit(f"{SID}: papa absent au 2e imprévu")
    for ban in (
        "éclat de citron",
        "éclat d'étal",
        "éclat de caisse",
        "éclat de cageot",
        "éclat de poire",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de gomme",
        "éclat de berge",
        "éclat de brouette",
        "éclat de couverture",
        "éclat de capuche",
        "éclat de paillasson",
        "éclat de fauteuil",
        "éclat de coffre",
        "éclat de haie",
        "éclat de housse",
        "tout doux",
        "tout calme",
        "toute calme",
        "merle",
        "miel",
        "sami",
        "cageot",
        "étal",
        "caisse",
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
    notes_ok = all(
        all(
            k in (c.get("notes") or "")
            for k in (
                "arc=",
                "intention=",
                "emotion=",
                "intensite=",
                "destinataire=",
                "sous_texte=",
                "tempo=",
                "sourire=",
                "respiration=",
            )
        )
        for c in chunks
    )
    if not notes_ok:
        raise SystemExit(f"{SID}: notes incomplètes")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)
    if not (700 <= nwords <= 850):
        raise SystemExit(f"{SID}: {nwords} mots (voulu 700–850)")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans\n"
        "- **Leçon :** EMO.LEX.003 — nommer la déception + chercher une "
        "autre idée (vécue : Nina veut le gâteau au citron **maintenant**, "
        "plateau vide, sourire parti, trou dans la poitrine, papa accroupi ; "
        "« Je suis déçue » ; 2e ruse : poire trop haute, presque prise, "
        "autre enfant, elle refuse de foncer, choisit une poire plus basse). "
        "JAMAIS dite dans le récit. Pas « on peut chercher une autre idée ». "
        "Pas « c'est de la déception ». Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Nina, papa, maman. Dump Sami/papa → D16 "
        "Nina = enfant-f (veut le gâteau maintenant). Pas de copain "
        "(dump sans camarade ; autre enfant non parlant au 2e imprévu). "
        "Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** marché, pavés, cagette, citron, gâteau, poire, sac, "
        "plateau, miettes, bois. Gâteau / citron / poire / marché = dump. "
        "≠ étal / caisse / cageot.\n"
        "- **Indice unique :** éclat de cagette (luit à l'ouverture → "
        "tremble à la déception → luit quand la poire bascule → tient "
        "sur le bois). BAN éclat de citron / étal / caisse / cageot / "
        "poire / treille / moule / tuteur / saladier / gomme / berge / "
        "brouette / couverture / capuche / paillasson / fauteuil / "
        "coffre / haie / housse.\n"
        "- **Question moteur :** « Le gâteau n'est plus là. Que dit "
        "Nina ? » expected dump **déçu**. accepted dump "
        "`déçu | je suis déçu | autre idée | une poire | une autre idée`. "
        "retry dump Sami → Nina (dit-elle). Non récitée dans les autres "
        "chunks. Hors Q : expected/accepted/retry restent **null**.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un citron échappe aux doigts de maman. Pavés, sac, cagette. "
        "Sur le bois, un éclat de cagette luit. Nina veut le gâteau "
        "**maintenant**. Plateau vide, miettes. Sourire parti. Trou "
        "dans la poitrine. Papa s'accroupit. Je suis déçue. Merci "
        "vécu. Une poire, alors. Deuxième ruse : poire trop haute, "
        "presque prise, autre enfant. Elle refuse de foncer. Poire "
        "plus basse, petite trace. Un éclat de cagette tient sur le "
        "bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, pavés froids, cagette de bois, citron, "
        "sac, plateau. ≠ étal / caisse / cageot.\n"
        "- Désir : le gâteau au citron, maintenant.\n"
        "- Objet : gâteau manquant, puis poire à la trace.\n"
        "- Indice unique : éclat de cagette, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de citron / étal / caisse / cageot / "
        "poire.\n"
        "- Urgence douce : elle avance trop vite vers le plateau.\n"
        "- Imprévu 1 : plateau vide, sourire parti, trou dans la "
        "poitrine.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "l'arrêt.\n"
        "- Imprévu 2 (plus rusé) : poire trop haute, presque prise, "
        "main d'un autre enfant.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "marché, retrouve l'éclat, choisit une poire plus basse.\n"
        "- Retour : poire contre le sac, petite trace, éclat sur le "
        "bois. Dénouement qui a failli : la poire partait plus haut.\n\n"
        "## Vécu\n\n"
        "Nina veut le gâteau **maintenant**. Impatience, puis plateau "
        "vide, sourire parti, trou dans la poitrine. Elle dit je suis "
        "déçue. Elle s'arrête, regarde les fruits, dit une poire. "
        "Papa se baisse, pose une question, ne récite pas la règle. "
        "Merci vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nina et le gâteau au citron (noyau dump). Relance : "
        "Que dit Nina ? expected déçu.\n"
        "- Lieu du dump-meta (marché). Maman et papa. "
        "Nina = héros enfant-f. Gâteau / citron / poire conservés.\n"
        "- Ouverture inventée (citron qui échappe, marché), pas un "
        "gabarit v2, pas « Sami marche au marché », pas « L'histoire "
        "est finie ».\n"
        "- Indice unique : éclat de cagette. BAN éclat de citron / "
        "étal / caisse / cageot / poire. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme/toute calme et "
        "`aujourd'hui` retirés. Strip « j'ai dit : je suis », "
        "« on peut chercher une autre idée », « c'est de la "
        "déception », « tu as nommé ».\n"
        "- Leçon non dite : on la voit quand le plateau est vide, "
        "quand Nina dit je suis déçue, quand elle choisit une poire. "
        "Pas « on peut chercher une autre idée ». Pas « c'est de la "
        "déception ». Pas « j'ai dit : je suis ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le gâteau n'est plus là. Que dit "
        "Nina ? ». expected déçu. 5 chunks, kinds inchangés. "
        "expected/accepted dump conservés (labels masculin moteur). "
        "retry Sami → Nina (dit-elle). Hors Q : null.\n"
        "- example4 068 / 100 / 032 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la poire trop haute.\n"
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
