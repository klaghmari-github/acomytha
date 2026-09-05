#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-08 — Le citron de Victorina (F-NAR-019, N2, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-08"
TITLE = "Le citron de Victorina"
N2 = LIMITS["N2"]
CHARS = "Victorina, papa, maman"
SETTING = (
    "marché, barquette, basilic, citron, fraises, panier, "
    "table, herbes, linge, plastique, verre"
)
INDICE = "éclat de barquette"
FIL = (
    "Une tige de basilic accroche la manche. Sur le plastique, "
    "un éclat de barquette luit. Victorina veut les fraises, "
    "maintenant. Les fraises, c'est pour plus tard. Sourire parti. "
    "Trou dans la poitrine. Papa s'accroupit. Je suis déçue. "
    "Merci vécu. Elle sent le basilic. Deuxième ruse : basilic "
    "qui glisse, citron trop acide. Elle refuse de foncer. "
    "Elle choisit un citron. Un éclat de barquette tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|gomme|berge|"
    r"brouette|couverture|capuche|paillasson|fauteuil|coffre|"
    r"haie|housse|cageot|étal|etal|caisse|cagette|kiosque|"
    r"gâteau|gateau|poire|pavés|paves|store|napperon|rail|"
    r"pelle|ficelle|maîtresse|maitresse|grand-père|grand-pere|"
    r"jardinier|bibliothécaire|bibliothecaire|gardienne|sami)\b",
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
    "éclat de fraise",
    "éclat de cagette",
    "éclat de kiosque",
    "éclat d'étal",
    "éclat d'etal",
    "éclat de caisse",
    "éclat de cageot",
    "éclat de store",
    "éclat de napperon",
    "éclat de rail",
    "éclat de pelle",
    "éclat de ficelle",
    "éclat de panier",
    "éclat de verre",
    "éclat de linge",
    "éclat de table",
    "éclat de plastique",
    "toute calme",
    "tout calme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de barquette",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_les_fraises_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Victorina",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_n_a_pas_les_fraises_que_dit_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="basilic",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_sent_le_basilic_sans_slogan; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de barquette",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=basilic_qui_glisse_citron_trop_acide_elle_choisit; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de barquette",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_plastique; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçue",
    "accepted_examples": (
        "déçue | je suis déçue | autre idée | le citron | le basilic"
    ),
    "retry_prompt": (
        "Elle dit je suis déçue. Puis elle cherche une autre idée. Que dit-elle ?"
    ),
    "engine_ok_text": "Oui, déçue.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "marché,basilic",
        [
            "narrateur|Une tige de basilic accroche la manche de Victorina.",
            "enfant-f|Elle pique, papa !",
            "papa|Tu la vois, la tige ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa détache la tige, près du panier.",
            "enfant-f|Elle sent le vert.",
            "maman|Tu la sens, Victorina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le marché sent les herbes, près des tables.",
            "enfant-f|Ça sent fort.",
            "papa|Tu le sens, le vert ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils avancent vers le passage des herbes.",
            "enfant-f|Des feuilles dans l'eau.",
            "maman|Tu les vois, les vertes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le basilic tremble dans un verre d'eau.",
            "enfant-f|Il tremble.",
            "papa|Tu le vois, le basilic ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une barquette de fraises attend, près du verre.",
            "enfant-f|Des rouges !",
            "maman|Tu les vois, les fraises ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur le plastique, un éclat de barquette luit.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un point clair.",
            "narrateur|Le plastique de la barquette est un peu froid.",
            "enfant-f|Il est froid.",
            "maman|Tes doigts sont bien, Victorina ?",
            "enfant-f|Un peu froids.",
            "narrateur|Un linge blanc cache d'autres fruits, plus loin.",
            "enfant-f|Il sent le soleil.",
            "papa|Tu le sens, le linge ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Victorina tend les deux mains.",
            "enfant-f|Je veux les fraises, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Victorina avance trop vite vers la barquette.",
            "narrateur|Ses doigts touchent seulement le plastique.",
            "maman|Les fraises, c'est pour plus tard.",
            "enfant-f|Maintenant !",
            "narrateur|Les rouges restent dans la barquette.",
            "enfant-f|Je les veux.",
            "maman|Plus tard, Victorina ?",
            "enfant-f|Non, maman.",
            "narrateur|Le sourire de Victorina disparaît.",
            "narrateur|Dans sa poitrine, l'envie des fraises fait un trou.",
            "narrateur|L'envie et le trou se bousculent sans place.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-f|J'ai mal au ventre.",
            "papa|Ta gorge est serrée, Victorina ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Papa s'accroupit à la même hauteur, sans parler.",
            "maman|Tes mains sont chaudes, Victorina ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|Je suis déçue.",
            "narrateur|L'éclat de barquette tremble, puis tient.",
            "narrateur|Victorina lève les yeux vers les herbes.",
            "enfant-f|Du basilic.",
            "papa|Tu le vois, Victorina ?",
            "enfant-f|Oui, papa.",
            "maman|Le panier reste près de toi ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina n'a pas les fraises.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "marché",
        [
            "narrateur|Victorina reste près de la barquette, un moment.",
            "enfant-f|Les fraises, maintenant.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Je les prends.",
            "narrateur|Victorina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Victorina refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe les herbes, un instant.",
            "narrateur|Elle écoute le marché, près des tables.",
            "papa|Tu restes un peu, Victorina ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Victorina.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le basilic sent fort, sous les doigts.",
            "enfant-f|Il est mouillé.",
            "narrateur|La poitrine de Victorina ralentit un peu.",
            "narrateur|Les épaules se relèvent un peu.",
            "enfant-f|On sent le basilic ?",
            "maman|Tu la froisses, la feuille ?",
            "enfant-f|Oui, maman.",
            "papa|Ça sent le vert, Victorina ?",
            "enfant-f|Ça pique un peu le nez.",
            "narrateur|Victorina froisse une feuille, sans se presser.",
            "enfant-f|Le vert, papa.",
            "papa|On s'approche sans se presser ?",
            "enfant-f|Oui.",
            "narrateur|Ils se lèvent, sans se bousculer.",
            "enfant-f|Le basilic, papa.",
            "papa|On y va, sans se presser.",
            "enfant-f|Un citron, aussi.",
            "maman|Tu le vois, le jaune ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "marché,citron",
        [
            "narrateur|Victorina lève la main vers le basilic.",
            "enfant-f|Je le prends !",
            "narrateur|La tige glisse entre ses doigts, trop mouillée.",
            "enfant-f|Il part !",
            "narrateur|Le basilic retombe dans l'eau, près du verre.",
            "narrateur|Victorina avance les mains, trop vite.",
            "enfant-f|Un citron, alors !",
            "narrateur|Elle porte un citron trop près du nez.",
            "narrateur|Le citron pique trop, trop acide.",
            "enfant-f|Il pique !",
            "narrateur|Victorina avance trop vite vers le jaune.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Victorina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le citron, un instant.",
            "narrateur|Elle écoute le marché, près de la barquette.",
            "narrateur|Sur le plastique, un éclat de barquette luit.",
            "enfant-f|Là, sur le plastique.",
            "papa|Tu vois le point, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le premier citron reste trop acide, trop près.",
            "enfant-f|Pas celui-là.",
            "maman|Tu en vois un autre, Victorina ?",
            "enfant-f|Plus rond.",
            "narrateur|Un citron plus rond attend à hauteur de main.",
            "enfant-f|Celui-là, maman.",
            "papa|Tu le prends, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Victorina choisit le citron plus rond, sans se presser.",
            "narrateur|La peau est lisse et froide.",
            "enfant-f|Il est lourd.",
            "maman|Il tient dans ta main ?",
            "enfant-f|Oui, maman.",
            "narrateur|Victorina le pose dans le panier.",
            "enfant-f|Mon citron.",
            "papa|Il a une petite trace, Victorina.",
            "enfant-f|Il a failli piquer.",
            "narrateur|Le citron sent le vert, un peu.",
            "enfant-f|Et le basilic, autour.",
            "papa|On reste près de la barquette ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la barquette.",
            "narrateur|Maman essuie un peu d'eau sur le plastique.",
            "enfant-f|Le citron a une trace, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, près du bord.",
            "maman|On est bien, ici.",
            "narrateur|Victorina tapote le plastique de la barquette.",
            "enfant-f|Il a une trace d'eau.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le citron est resté, Victorina.",
            "enfant-f|Oui, avec nous.",
            "narrateur|Le citron roule dans le panier, presque dehors.",
            "enfant-f|Il bascule !",
            "narrateur|Puis il tient, contre le tissu du panier.",
            "narrateur|Ça sent le basilic, un peu tiède.",
            "enfant-f|Et le plastique, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le marché sent les herbes, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le citron reste contre le panier.",
            "narrateur|Un éclat de barquette tient sur le plastique.",
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
        raise SystemExit(f"{SID}: enfant-m (Victorina = enfant-f)")
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
    if q["text"] != "Victorina n'a pas les fraises. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçue":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "déçue | je suis déçue | autre idée | le citron | le basilic"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != (
        "Elle dit je suis déçue. Puis elle cherche une autre idée. Que dit-elle ?"
    ):
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
    if "basilic" not in by["CHK_T0000_P0000_C0001"]["text"].lower():
        raise SystemExit(f"{SID}: basilic absent après la question")
    if "fraise" not in blob:
        raise SystemExit(f"{SID}: manque fraises")
    if "citron" not in blob:
        raise SystemExit(f"{SID}: manque citron")
    if "basilic" not in blob:
        raise SystemExit(f"{SID}: manque basilic")
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
    if "trop acide" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (trop acide)")
    if "glisse" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (basilic qui glisse)")
    if "choisit" not in end_txt:
        raise SystemExit(f"{SID}: manque citron choisi")
    if "papa" not in by["CHK_T0000_P0000_END"]["script"].lower():
        raise SystemExit(f"{SID}: papa absent au 2e imprévu")
    for ban in (
        "éclat de citron",
        "éclat de fraise",
        "éclat de cagette",
        "éclat de kiosque",
        "éclat d'étal",
        "éclat de caisse",
        "éclat de cageot",
        "éclat de store",
        "éclat de napperon",
        "éclat de rail",
        "éclat de pelle",
        "éclat de ficelle",
        "tout doux",
        "tout calme",
        "toute calme",
        "merle",
        "miel",
        "sami",
        "cageot",
        "étal",
        "caisse",
        "cagette",
        "kiosque",
        "gâteau",
        "gateau",
        "poire",
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
        "autre idée (vécue : Victorina veut les fraises **maintenant**, "
        "fraises pour plus tard, sourire parti, trou dans la poitrine, "
        "papa accroupi ; « Je suis déçue » ; elle sent le basilic ; "
        "2e ruse : basilic qui glisse, citron trop acide, elle refuse "
        "de foncer, choisit un citron plus rond). JAMAIS dite dans le "
        "récit. Pas « on peut chercher une autre idée ». Pas « c'est de "
        "la déception ». Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Victorina, papa, maman. Dump maman seulement "
        "→ **ajoute papa**. Victorina = enfant-f (veut les fraises "
        "maintenant). Pas de copain. Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** marché, barquette, basilic, citron, fraises, panier, "
        "table, herbes, linge, plastique, verre. Fraises / basilic / "
        "citron / marché = dump. ≠ cagette / kiosque / étal / cageot. "
        "≠ gâteau / poire (003-01).\n"
        "- **Indice unique :** éclat de barquette (luit à l'ouverture → "
        "tremble à la déception → luit quand le basilic glisse et le "
        "citron pique → tient sur le plastique). BAN éclat de citron / "
        "fraise / cagette / kiosque / étal / caisse / cageot / store / "
        "napperon / rail / pelle / ficelle.\n"
        "- **Question moteur :** « Victorina n'a pas les fraises. Que "
        "dit-elle ? » expected dump **déçue**. accepted dump "
        "`déçue | je suis déçue | autre idée | le citron | le basilic`. "
        "retry dump conservé. Non récitée dans les autres chunks. Hors "
        "Q : expected/accepted/retry restent **null**.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une tige de basilic accroche la manche. Passage des herbes, "
        "verre d'eau, barquette. Sur le plastique, un éclat de barquette "
        "luit. Victorina veut les fraises **maintenant**. Les fraises, "
        "c'est pour plus tard. Sourire parti. Trou dans la poitrine. "
        "Papa s'accroupit. Je suis déçue. Merci vécu. Elle sent le "
        "basilic. Deuxième ruse : basilic qui glisse, citron trop acide. "
        "Elle refuse de foncer. Citron plus rond, petite trace. Le "
        "citron roule, presque dehors, puis tient. Un éclat de "
        "barquette tient sur le plastique.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, passage des herbes, barquette, verre, linge, "
        "panier. ≠ cagette / kiosque / étal / cageot.\n"
        "- Désir : les fraises, maintenant.\n"
        "- Objet : fraises pour plus tard, puis basilic senti, puis "
        "citron choisi.\n"
        "- Indice unique : éclat de barquette, vu dès l'ouverture, payé "
        "sur le plastique. Pas éclat de citron / fraise / cagette / "
        "kiosque / étal / cageot / store / napperon / rail / pelle / "
        "ficelle.\n"
        "- Urgence douce : elle avance trop vite vers la barquette.\n"
        "- Imprévu 1 : fraises pour plus tard, sourire parti, trou dans "
        "la poitrine.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après l'arrêt.\n"
        "- Imprévu 2 (plus rusé) : basilic qui glisse, citron trop acide.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "marché, retrouve l'éclat, choisit un citron plus rond.\n"
        "- Retour : citron contre le panier, petite trace, il a failli "
        "sortir. Éclat sur le plastique. Dénouement qui a failli.\n\n"
        "## Vécu\n\n"
        "Victorina veut les fraises **maintenant**. Impatience, puis "
        "fraises pour plus tard, sourire parti, trou dans la poitrine. "
        "Elle dit je suis déçue. Elle s'arrête, sent le basilic, "
        "choisit un citron. Papa se baisse, pose une question, ne "
        "récite pas la règle. Merci vécu. Fin : l'éclat du début tient "
        "sur le plastique.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le citron de Victorina (noyau dump). Relance : "
        "Victorina n'a pas les fraises. Que dit-elle ? expected déçue.\n"
        "- Lieu du dump-meta (marché). Maman et papa (papa ajouté). "
        "Victorina = héros enfant-f. Fraises / basilic / citron "
        "conservés. Distinct de 003-01 (pas de gâteau, pas de poire, "
        "pas de cagette).\n"
        "- Ouverture inventée (tige de basilic à la manche), pas un "
        "gabarit v2, pas « La balance du marché fait tic », pas "
        "« L'histoire est finie ».\n"
        "- Indice unique : éclat de barquette ×4. BAN éclat de citron / "
        "fraise / cagette / kiosque / étal / cageot / store / napperon / "
        "rail / pelle / ficelle. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme/toute calme et "
        "`aujourd'hui` retirés. Strip « j'ai dit : je suis », "
        "« on peut chercher une autre idée », « c'est de la "
        "déception », « tu as nommé ».\n"
        "- Leçon non dite : on la voit quand les fraises restent, "
        "quand Victorina dit je suis déçue, quand elle sent le "
        "basilic, quand elle choisit un citron. Pas « on peut "
        "chercher une autre idée ». Pas « c'est de la déception ». "
        "Pas « j'ai dit : je suis ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Victorina n'a pas les fraises. Que "
        "dit-elle ? ». expected déçue. 5 chunks, kinds inchangés. "
        "expected/accepted/retry dump conservés. Hors Q : null.\n"
        "- example4 075 / 007 / 039 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le basilic qui glisse.\n"
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
