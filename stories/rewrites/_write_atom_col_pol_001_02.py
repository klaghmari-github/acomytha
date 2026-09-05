#!/usr/bin/env python3
"""ATOM-COL.POL.001-02 — Le gâteau au citron de Chouchou (F-NAR-019, N2, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-02"
TITLE = "Le gâteau au citron de Chouchou"
N2 = LIMITS["N2"]
CHARS = "Chouchou, papa, maman"
SETTING = (
    "visite chez la voisine. Cuisine collante de zeste, fils jaunes, "
    "gâteau tiède, escalier à la cire, palier, thé à la menthe"
)
INDICE = "éclat de zeste"
FIL = (
    "Des fils jaunes collent au bois. Sur le gâteau, un éclat de zeste "
    "brille. Chouchou veut donner le plat maintenant. Elle saisit trop "
    "vite : l'éclat glisse. À la porte, elle avance trop vite : les mains "
    "n'attrapent pas, les mots se perdent. Elle refuse de foncer, attend, "
    "dit s'il te plaît. Merci vécu. Un bout trop vite : la cuillère glisse. "
    "Elle refuse, demande. Sur le bois, l'éclat de zeste tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(pavé|pave|pli|mie|poisson|page|escargot|pompon|manteau|"
    r"seau|carton|mousse|carotte)\b",
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
    "zoé",
    "zoe",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "on aime écouter",
    "on aime ecouter",
    "tu as bien écouté",
    "tu as bien ecoute",
    "tu as bien fait",
    "bon travail",
    "tu as dit les mots",
    "les trois mots",
    "on dit bonjour",
    "on dit au revoir",
    "tu as suivi",
    "boulangerie",
    "éclat de citron",
    "éclat de pavé",
    "éclat de pave",
    "éclat de pli",
    "éclat de mie",
    "éclat de poisson",
    "éclat de page",
    "éclat d'escargot",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de carotte",
    "éclat de tapis",
    "éclat de buée",
    "éclat de buee",
    "éclat de crayon",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de casserole",
    "éclat de wagon",
    "éclat de nappe",
    "éclat de vitre",
    "éclat de tasse",
    "éclat de goutte",
    "éclat de laine",
    "éclat de grain",
    "éclat de liste",
    "éclat de sonnette",
    "éclat de parapluie",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "grain de miette",
    "grain de sable",
    "marque fine",
    "minuscule symbole",
    "ombre en forme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de zeste",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_donner_le_gateau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="gâteau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_dit_s_il_te_plait_en_tendant_le_plat; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="S'il te plaît",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_puis_tend_le_plat; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="cuillère",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sur_la_cuillere; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de zeste",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "s'il te plaît",
    "accepted_examples": (
        "s'il te plaît | merci | bonjour | s'il te plait"
    ),
    "retry_prompt": "Elle dit s'il te plaît et merci. Que dit Chouchou ?",
    "engine_ok_text": "Oui, s'il te plaît.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "porte,pas",
        [
            "narrateur|Des fils jaunes collent au bois de la table.",
            "narrateur|La table de la cuisine est collante de zeste.",
            "narrateur|Chouchou connaît cette cuisine, un peu collante.",
            "narrateur|Le gâteau au citron est tiède, tout rond.",
            "maman|Une goutte de glace brille sur la cuillère.",
            "enfant-f|Elle brille, maman.",
            "papa|On porte le plat à deux ?",
            "enfant-f|Oui, mes deux mains.",
            "maman|Le torchon est dessous.",
            "enfant-f|Il est doux.",
            "narrateur|Sur le gâteau, un éclat de zeste brille.",
            "enfant-f|Il est jaune, papa !",
            "papa|C'est le zeste, sur le dessus.",
            "enfant-f|Je le donne, maintenant !",
            "maman|Pendant que le plat est chaud ?",
            "enfant-f|Oui, tout de suite !",
            "narrateur|Chouchou saisit le plat trop vite.",
            "narrateur|Le plat penche vers le bord.",
            "narrateur|L'éclat de zeste glisse sur la glace.",
            "enfant-f|Oh.",
            "papa|Tes deux mains, Chouchou ?",
            "narrateur|Papa remet le plat droit.",
            "enfant-f|Oui, papa.",
            "maman|Le torchon reste dessous ?",
            "enfant-f|Oui, maman.",
            "papa|On monte ?",
            "enfant-f|On monte.",
            "narrateur|L'escalier de l'immeuble sent la cire.",
            "narrateur|Chaque marche fait un petit bruit de bois.",
            "papa|Tu tiens le plat, Chouchou ?",
            "enfant-f|Il est lourd un peu.",
            "maman|Je suis juste derrière toi.",
            "narrateur|Le paillasson a une petite fleur brodée.",
            "narrateur|En ce moment, Chouchou est devant la porte.",
            "papa|On sonne, une fois ?",
            "enfant-f|Oui, une fois.",
            "narrateur|La porte s'ouvre sur le palier.",
            "narrateur|Une odeur de thé à la menthe sort.",
            "enfant-f|Bonjour.",
            "papa|Bonjour.",
            "narrateur|La voisine ouvre plus grand.",
            "enfant-f|C'est pour vous, maintenant !",
            "narrateur|Chouchou avance le plat trop vite.",
            "narrateur|Le plat penche vers les mains ouvertes.",
            "narrateur|Les mains ne le prennent pas.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Tu le donnes, Chouchou ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "enfant-f|Oui, papa.",
            "narrateur|Les mots se perdent près de la porte.",
            "narrateur|Personne n'entend la fin.",
            "narrateur|Chouchou referme la bouche, un instant.",
            "narrateur|Le plat reste lourd, tout chaud.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou donne le gâteau.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "porte,verre",
        [
            "narrateur|Chouchou avance le plat trop vite.",
            "enfant-f|Le gâteau, le citron, pour vous !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Les mains ouvertes n'attrapent pas le plat.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Chouchou refuse de foncer.",
            "narrateur|Elle recule le plat, un peu.",
            "papa|Le plat est chaud, Chouchou ?",
            "narrateur|Papa reste à sa hauteur.",
            "maman|La fleur du paillasson est sous tes pieds.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Chouchou attend que le silence arrive.",
            "narrateur|Sur le dessus, l'éclat de zeste brille.",
            "enfant-f|Il est là.",
            "enfant-f|S'il te plaît.",
            "enfant-f|C'est pour vous.",
            "narrateur|Le plat passe dans des mains calmes.",
            "narrateur|Le plat n'est plus lourd.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Un verre d'eau arrive, tout clair.",
            "enfant-f|Merci.",
            "maman|Tu as soif, un peu ?",
            "enfant-f|Un peu, maman.",
            "papa|Tu parles du parc, si tu veux ?",
            "enfant-f|Les balançoires sont vertes.",
            "maman|On rentre, Chouchou ?",
            "enfant-f|Au revoir.",
            "narrateur|Une lumière jaune vient de la porte ouverte.",
            "narrateur|L'odeur de citron reste dans l'escalier.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pas,table",
        [
            "narrateur|Chouchou redescend l'escalier avec papa et maman.",
            "narrateur|Le bois ciré sent la cire, un peu.",
            "narrateur|Le citron reste dans l'air.",
            "enfant-f|Le plat n'est plus lourd, papa.",
            "papa|Elle l'a pris, oui.",
            "narrateur|À la maison, la table a des zestes.",
            "narrateur|La cuillère brille près du bois collant.",
            "enfant-f|Je prends un bout, maintenant !",
            "narrateur|Chouchou avance la main trop vite.",
            "narrateur|La cuillère glisse vers le bord.",
            "enfant-f|Oh.",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|La table est collante, Chouchou.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Elle écoute la cuisine, un instant.",
            "narrateur|Elle pose la main, sans presser.",
            "enfant-f|S'il te plaît, un bout ?",
            "maman|Oui, un petit.",
            "enfant-f|Il est tiède, maman.",
            "papa|Tu restes un peu ?",
            "enfant-f|Oui, papa.",
            "maman|Le torchon est près de l'évier.",
            "enfant-f|On le met ?",
            "papa|Oui, dans l'eau.",
            "narrateur|Le bout de gâteau sent le citron.",
            "enfant-f|Il colle aux doigts.",
            "maman|Comme la table, oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "table,cuisine",
        [
            "narrateur|Ils restent près de la table collante.",
            "narrateur|Les fils jaunes tiennent sur le bois.",
            "enfant-f|Comme sur le gâteau, papa.",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur le bois.",
            "maman|On est bien, ici.",
            "narrateur|Chouchou glisse le doigt, sans se presser.",
            "enfant-f|On le sent, maman.",
            "maman|Tu le sens sur tes doigts ?",
            "enfant-f|Oui, il colle.",
            "papa|Le plat est rentré vide.",
            "enfant-f|Oui, elle l'a pris.",
            "narrateur|L'odeur de citron reste dans la cuisine.",
            "enfant-f|Il est là, maman.",
            "maman|Oui, sur le bois.",
            "narrateur|L'éclat de zeste tient sur le bois.",
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "s'il te plaît" not in blob:
        raise SystemExit(f"{SID}: manque s'il te plaît vécu")
    if "zoé" in blob or "zoe" in blob:
        raise SystemExit(f"{SID}: Zoé restée")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Chouchou = enfant-f)")
    if "que dit-il" in blob:
        raise SystemExit(f"{SID}: Que dit-il ? (fille)")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "éclat de citron" in blob:
        raise SystemExit(f"{SID}: éclat de citron (BAN RAN.001-08)")
    q = by["CHK_T0000_P0000_Q0001"]
    if q.get("retry_prompt") and "zoé" in str(q["retry_prompt"]).lower():
        raise SystemExit(f"{SID}: Zoé dans retry")
    if "zoe" in str(q.get("retry_prompt") or "").lower():
        raise SystemExit(f"{SID}: Zoe dans retry")
    if "que dit-elle" not in q["text"].lower():
        raise SystemExit(f"{SID}: question moteur pas au féminin")
    if q.get("expected_answer") != "s'il te plaît":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if "chouchou" not in str(q.get("retry_prompt") or "").lower():
        raise SystemExit(f"{SID}: retry sans Chouchou")
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
        "- **Public :** N2 (4–5 ans), audio familial, ≤15 mots/phrase\n"
        "- **Leçon :** COL.POL.001 — s'il te plaît (et merci lié au verre "
        "d'eau du dump), vécue : veut donner le gâteau maintenant ; "
        "première idée échoue ; refuse de foncer ; dit s'il te plaît. "
        "Jamais dite comme règle.\n"
        "- **Personnages :** Chouchou, papa, maman. Troupe D16. Dump Zoé "
        "→ INTERDIT BAD_NAMES. `enfant-f`. Pas de maîtresse (absente du "
        "dump, non inventée). Adultes parlants = papa/maman. Voisine "
        "narrée, sans réplique.\n"
        "- **Lieu :** visite chez la voisine. Cuisine collante de zeste, "
        "fils jaunes, gâteau tiède, escalier à la cire, palier, thé à la "
        "menthe. ≠ POL.001-01 (boulangerie / pavé / petit pain).\n"
        "- **Indice unique :** éclat de zeste (gâteau → glisse sur la "
        "glace → brille au silence du palier → tient sur le bois). Pas "
        "éclat de citron (BAN RAN.001-08).\n"
        "- **Question moteur :** « Chouchou donne le gâteau. Que dit-elle ? » "
        "(dump : Que dit-il ?). expected **s'il te plaît**. retry "
        "Zoé→Chouchou.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Des fils jaunes collent au bois. Table collante de zeste. Gâteau "
        "tiède, goutte de glace, torchon doux. Sur le gâteau, un éclat de "
        "zeste brille. Chouchou veut le donner **maintenant**. Elle saisit "
        "trop vite : l'éclat glisse, le plat penche. Papa remet droit. "
        "Escalier à la cire, paillasson à fleur. En ce moment, elle est "
        "devant la porte. Menthe. Bonjour. Elle avance trop vite : les "
        "mains n'attrapent pas. Sourire parti. Papa s'accroupit. Les mots "
        "se perdent. Elle refuse de foncer, attend le silence, dit s'il "
        "te plaît. Le plat n'est plus lourd. Merci vécu. Verre d'eau, "
        "merci enfant. Au revoir. À la maison, un bout trop vite : la "
        "cuillère glisse. Elle refuse, demande. Sur le bois, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine au zeste, fils jaunes, gâteau au citron, "
        "escalier ciré, palier, thé à la menthe. ≠ 001-01 boulangerie/"
        "pavé.\n"
        "- Désir : donner le plat chaud à la voisine, maintenant.\n"
        "- Objet : gâteau au citron, plat, torchon, cuillère.\n"
        "- Indice unique : éclat de zeste, vu dès l'ouverture, payé au "
        "climax (dessus pendant le silence) et sur le bois au retour.\n"
        "- Urgence douce : le plat chaud, les mains ouvertes.\n"
        "- Imprévu 1 : tout de suite, plat trop vite, éclat qui glisse, "
        "mots perdus à la porte.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la phrase "
        "entière sur le palier.\n"
        "- Imprévu 2 (plus rusé) : à la maison, un bout maintenant ; la "
        "cuillère glisse, les voix se mélangent.\n"
        "- Résolution : elle refuse de foncer, attend, dit s'il te plaît, "
        "demande un bout.\n"
        "- Retour : fils jaunes, doigt sans se presser, l'éclat tient sur "
        "le bois.\n\n"
        "## Vécu\n\n"
        "Leçon COL.POL.001 (s'il te plaît pour donner, merci pour l'eau) "
        "greffée, jamais annoncée. La première idée (tendre d'un coup) "
        "échoue. Le choix de Chouchou change l'action. Un « en ce moment ». "
        "Un merci vécu. Adulte + question. Troupe D16 : Chouchou, papa, "
        "maman. N2.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le gâteau au citron de Chouchou (noyau dump).\n"
        "- Héros Chouchou, fille. Dump Zoé → INTERDIT. `enfant-f`. "
        "Retry Zoé→Chouchou.\n"
        "- Maman ajoutée (dump : Zoé, papa). Pas de maîtresse inventée.\n"
        "- Question moteur : « Chouchou donne le gâteau. Que dit-elle ? » "
        "(dump : Que dit-il ?). Fond s'il te plaît conservé.\n"
        "- Ouverture inventée (fils jaunes sur le bois), pas un gabarit "
        "v2, pas « va à l'école ».\n"
        "- Indice unique : éclat de zeste. Pas pavé/pli/mie/poisson/page/"
        "escargot/pompon/manteau/seau/carton/mousse/carotte, pas éclat de "
        "citron.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés.\n"
        "- Interdit « bon travail / histoire finie / tu as dit les mots / "
        "les trois mots / on dit bonjour ».\n"
        "- 5 chunks, kinds inchangés. example4 : 066, 098, 030.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
