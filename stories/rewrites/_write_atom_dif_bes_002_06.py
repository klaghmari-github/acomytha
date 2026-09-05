#!/usr/bin/env python3
"""ATOM-DIF.BES.002-06 — Les bateaux de la cour (F-NAR-019, N2, DIF.BES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.002-06"
TITLE = "Les bateaux de la cour"
N2 = LIMITS["N2"]
CHARS = "Aniss, Chouchou, papa, maman"
SETTING = "cour après la pluie, gouttière de zinc, flaque des dalles"
INDICE = "éclat de dalle"
FIL = (
    "L'air froid glisse le long du zinc. Sur une dalle, un éclat de "
    "dalle brille. Aniss veut faire courir les bateaux jusqu'à l'éclat, "
    "maintenant. Il propose. Chouchou regarde, puis dit plus tard. Le "
    "bateau s'arrête sur une feuille. Sourire parti. Aniss refuse de "
    "foncer, accepte, dégage le bateau. Merci vécu. Deux bateaux trop "
    "vite : ils se cognent. L'éclat de dalle tient au bout de la flaque."
)
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
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "tu attends ton tour",
    "on peut proposer",
    "tu as proposé",
    "tu as propose",
    "tu as accepté",
    "tu as accepte",
    "accepter plusieurs",
    "plusieurs réponses",
    "plusieurs reponses",
    "on peut accepter",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "éclat de gouttière",
    "éclat de gouttiere",
    "eclat de gouttiere",
    "éclat de zinc",
    "éclat de cour",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de pompon",
    "éclat de laine",
    "éclat de tasse",
    "éclat de carton",
    "éclat de mousse",
    "éclat de seau",
    "éclat de carotte",
    "éclat de galet",
    "éclat de couloir",
    "éclat de cube",
    "éclat de bois",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de carte",
    "éclat de boule",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de dalle",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_les_bateaux_jusqu_a_l_eclat_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="plus tard",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=chouchou_dit_plus_tard_aniss_accepte; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="D'accord",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_tirer_dit_d_accord; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de dalle",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=deux_bateaux_trop_vite_il_observe_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de dalle",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_au_bout_de_la_flaque; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "accepter",
    "accepted_examples": (
        "accepter | d'accord | proposer | regarder | plus tard"
    ),
    "retry_prompt": "Il accepte. Que fait Aniss ?",
    "engine_ok_text": "Oui, il accepte.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pluie,cour",
        [
            "narrateur|L'air froid glisse le long du zinc.",
            "narrateur|Aniss connaît cette cour, ses dalles, le bruit de la gouttière.",
            "narrateur|Un détail paraît nouveau, sur une dalle sombre.",
            "narrateur|Au bout de la flaque, un éclat de dalle brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur la dalle ?",
            "enfant-m|Oui, tout au bout.",
            "narrateur|Ça sent la pierre mouillée.",
            "narrateur|Maman pose un torchon sur le rebord.",
            "maman|Tu as vu l'éclat, Aniss ?",
            "enfant-m|Oui, maman.",
            "narrateur|Deux bateaux de papier attendent.",
            "narrateur|Ils sont un peu froissés.",
            "narrateur|Papa les a pliés, ce matin.",
            "papa|Ils peuvent flotter dans la flaque.",
            "enfant-m|Je veux les faire courir, maintenant !",
            "enfant-m|Jusqu'à l'éclat, le long des dalles.",
            "maman|Le long des dalles ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un escargot avance sur une fissure.",
            "enfant-m|Il a une petite maison.",
            "papa|On le laisse sur sa fissure ?",
            "enfant-m|Oui, papa.",
            "narrateur|Chouchou est sur la marche sèche.",
            "narrateur|Ses chaussettes restent au sec.",
            "narrateur|Elle tient le torchon, près du rebord.",
            "maman|Tu as le torchon, Chouchou ?",
            "enfant-f|Oui, maman.",
            "narrateur|Aniss le voit, sur la marche.",
            "enfant-m|Tu viens ?",
            "enfant-m|On fait courir les bateaux.",
            "narrateur|Chouchou penche la tête.",
            "narrateur|Elle ne descend pas.",
            "enfant-f|Je regarde.",
            "narrateur|Aniss écoute.",
            "enfant-m|D'accord.",
            "narrateur|En ce moment, Aniss pose un bateau.",
            "narrateur|Le papier devient sombre.",
            "narrateur|Il boit un peu d'eau.",
            "enfant-m|Il part !",
            "narrateur|Aniss pousse trop vite, du doigt.",
            "narrateur|Le bateau glisse entre deux dalles.",
            "narrateur|L'escargot s'écarte, très lent.",
            "enfant-m|Il laisse passer !",
            "narrateur|Une feuille collée barre le chemin.",
            "narrateur|Le bateau s'arrête, loin de l'éclat.",
            "enfant-m|Il est coincé !",
            "enfant-m|Il n'arrive pas au bout.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|L'éclat de dalle tremble, puis tient.",
            "narrateur|Les épaules d'Aniss tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu vois la feuille ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss cherche autour de la flaque.",
            "narrateur|Il regarde Chouchou.",
            "enfant-m|Tu m'aides ?",
            "narrateur|Chouchou serre le torchon.",
            "narrateur|Elle reste sur la marche.",
            "enfant-f|Plus tard.",
            "narrateur|Aniss ouvre la bouche.",
            "narrateur|Puis il la referme.",
            "narrateur|Ça serre, dans son ventre.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou dit plus tard.",
            "narrateur|Que fait Aniss ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "flaque,bateaux",
        [
            "narrateur|Aniss veut tirer Chouchou vers l'eau.",
            "enfant-m|Viens, maintenant !",
            "narrateur|Chouchou recule d'un pas, sur la marche.",
            "enfant-f|Plus tard.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Il referme la main.",
            "narrateur|Il écoute la marche, un instant.",
            "enfant-m|D'accord.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu restes près de la flaque ?",
            "enfant-m|Oui, papa.",
            "narrateur|Maman se baisse aussi.",
            "maman|Merci, Aniss.",
            "narrateur|Maman a entendu toute la phrase.",
            "narrateur|Aniss prend une petite brindille.",
            "narrateur|Elle est lisse, un peu mouillée.",
            "narrateur|Il pousse la feuille, sans se presser.",
            "narrateur|Le bateau se dégage.",
            "enfant-m|Il repart !",
            "papa|Il glisse ?",
            "enfant-m|Oui, papa.",
            "narrateur|Chouchou reste sur la marche.",
            "narrateur|Elle penche la tête.",
            "narrateur|Le deuxième bateau attend au sec.",
            "enfant-f|Je mets une voile ?",
            "enfant-m|Si tu veux.",
            "narrateur|Chouchou pose une feuille sèche.",
            "narrateur|C'est une voile, sur le papier.",
            "narrateur|Elle ne descend pas dans l'eau.",
            "papa|Tu vois la voile ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux bateaux glissent.",
            "narrateur|Ils font deux ronds dans la flaque.",
            "enfant-m|Ils se croisent !",
            "papa|Ils arrivent au bout ?",
            "enfant-m|Presque, papa.",
            "narrateur|L'escargot a fini sa fissure.",
            "narrateur|Le ventre d'Aniss se desserre.",
            "maman|Tu as les mains froides ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "flaque,zinc",
        [
            "narrateur|Aniss veut les deux bateaux, d'un coup.",
            "enfant-m|Tous les deux, jusqu'à l'éclat !",
            "narrateur|Il pousse trop vite.",
            "narrateur|Les bateaux se cognent.",
            "narrateur|L'un tourne, loin de la dalle.",
            "enfant-m|Oh.",
            "narrateur|La voile se couche.",
            "enfant-m|Il n'arrive pas !",
            "narrateur|Aniss avance la main.",
            "narrateur|Puis il s'arrête net.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Aniss observe la flaque.",
            "narrateur|Il écoute le zinc, une goutte.",
            "narrateur|Au bout, un éclat de dalle luit.",
            "enfant-m|Là, sur la dalle.",
            "narrateur|Aniss tient la brindille des deux mains.",
            "narrateur|La brindille est froide, un peu lisse.",
            "enfant-m|Elle est froide, papa.",
            "papa|Tu le guides jusqu'à l'éclat ?",
            "enfant-m|Oui, papa.",
            "maman|On avance ?",
            "enfant-m|Oui, maman.",
            "narrateur|Aniss pousse sans se presser.",
            "narrateur|Le bateau glisse vers la dalle.",
            "narrateur|L'air froid revient sur les joues.",
            "narrateur|Chouchou souffle, depuis la marche.",
            "enfant-f|Fffff.",
            "narrateur|La voile se relève un peu.",
            "enfant-m|Il arrive.",
            "papa|On marche.",
            "narrateur|Le papier touche l'éclat, tout au bout.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "zinc,dalles",
        [
            "enfant-m|Mes bateaux ont couru, papa.",
            "papa|Tu les vois, sur le rebord ?",
            "enfant-m|Oui, comme tout à l'heure.",
            "narrateur|Aniss pose un bateau sur le rebord.",
            "narrateur|Chouchou pose l'autre.",
            "narrateur|Le papier sèche un peu.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur la dalle.",
            "maman|On est bien, ici.",
            "enfant-f|Mes chaussettes sont sèches.",
            "enfant-m|Les miennes sont un peu mouillées.",
            "maman|On les change après ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une goutte quitte le zinc.",
            "narrateur|Elle fait un rond dans la flaque.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur la dalle ?",
            "enfant-m|Oui, l'éclat.",
            "narrateur|Le soir reste dans l'air.",
            "narrateur|Au bout de la flaque, l'éclat de dalle tient.",
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
    if "copain|" in blob or "copine|" in blob:
        raise SystemExit(f"{SID}: copain/copine")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: Chouchou = enfant-f manquant")
    if "plus tard" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: plus tard absent à l'ouverture")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Chouchou dit plus tard. Que fait Aniss ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "accepter":
        raise SystemExit(f"{SID}: expected_answer altéré")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut proposer",
        "tu as proposé",
        "tu as accepté",
        "accepter plusieurs",
        "plusieurs réponses",
        "on peut accepter",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
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
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter / proposer / accepter (vécue : "
        "Aniss propose les bateaux ; Chouchou regarde, puis dit plus tard ; "
        "le bateau n'arrive pas au bout ; Aniss veut tirer, refuse de foncer, "
        "dit d'accord ; merci vécu ; deux bateaux trop vite se cognent ; "
        "il observe l'éclat)\n"
        "- **Personnages :** Aniss, Chouchou, papa, maman. Troupe D16. "
        "Aniss = enfant-m. Chouchou = enfant-f (rythme plus lent, marche "
        "sèche). Adultes parlants = papa/maman.\n"
        "- **Lieu :** cour après la pluie, gouttière de zinc, flaque des "
        "dalles, rebord, torchon, escargot. ≠ DIF.BES.002-01..05 (plaque, "
        "pierre, grille, couvercle, cheminée).\n"
        "- **Indice unique :** éclat de dalle (dalle au bout de la flaque → "
        "tremble quand le bateau s'arrête → luit après le choc → tient au "
        "bout). Pas éclat de gouttière. Pas point de gouttière. Pas éclat "
        "de cour (BAN 001-08). Pas éclat de zinc.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "L'air froid glisse le long du zinc. Sur une dalle sombre, un éclat "
        "de dalle brille. Aniss veut faire courir les bateaux **maintenant**, "
        "jusqu'à l'éclat. Il propose : tu viens. Chouchou, sur la marche "
        "sèche, dit je regarde. Aniss écoute. En ce moment il pose un "
        "bateau, pousse trop vite : une feuille barre le chemin, le bateau "
        "n'arrive pas au bout. Sourire parti, épaules basses. Papa se "
        "baisse. Tu m'aides. Chouchou : plus tard. Aniss referme la bouche. "
        "Il refuse de foncer, dit d'accord, dégage le bateau d'une "
        "brindille. Merci vécu. Chouchou pose une voile depuis la marche. "
        "Deux bateaux trop vite se cognent. Il observe, écoute le zinc, "
        "retrouve l'éclat. Au bout de la flaque, l'éclat de dalle tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cour après la pluie, zinc, dalles sombres, flaque, "
        "torchon, escargot, marche sèche, bateaux froissés.\n"
        "- Désir : faire courir les bateaux jusqu'à l'éclat **maintenant**.\n"
        "- Objet : bateaux de papier, brindille, feuille-voile, torchon.\n"
        "- Indice unique : éclat de dalle, vu dès l'ouverture, payé au bout "
        "de la flaque.\n"
        "- Urgence douce : Chouchou reste au sec, le bateau n'atteint pas "
        "le bout promis.\n"
        "- Imprévu 1 : poussée trop vite, feuille collée, bateau coincé.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après d'accord.\n"
        "- Imprévu 2 (plus rusé) : les deux bateaux d'un coup se cognent ; "
        "la voile se couche.\n"
        "- Résolution : il refuse de foncer, accepte plus tard, observe "
        "l'éclat, guide sans se presser.\n"
        "- Retour : bateaux sur le rebord, goutte du zinc, éclat qui tient.\n\n"
        "## Vécu\n\n"
        "Aniss veut les bateaux **maintenant**. Impatience (propose, pousse "
        "trop vite, veut tirer Chouchou), puis sourire qui disparaît, "
        "épaules qui tombent, bouche refermée. Chouchou a un autre rythme : "
        "je regarde, plus tard, voile depuis la marche, silence qui compte. "
        "Papa se baisse, pose une question, ne récite pas la règle. Aniss "
        "agit : main refermée, d'accord, brindille, puis il s'arrête net. "
        "Merci vécu après la phrase. Fin : l'éclat du début tient au bout "
        "de la flaque.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : Les bateaux de la cour. Lieu du dump : cour après "
        "la pluie, gouttière de zinc, flaque des dalles. Relance : "
        "Chouchou dit plus tard. Que fait Aniss ? expected accepter.\n"
        "- Ouverture inventée (l'air froid le long du zinc), pas un "
        "gabarit v2, pas « joue au salon ».\n"
        "- Indice unique : éclat de dalle (roster). Pas plaque/pierre/"
        "grille/couvercle/cheminée, pas éclat de gouttière, pas point de "
        "gouttière, pas éclat de cour, pas éclat de zinc, pas merle, miel, "
        "marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : on l'entend quand il dit d'accord et reste "
        "près de la flaque. Pas « on peut proposer », pas « tu as "
        "accepté », pas « accepter plusieurs réponses ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Deux rythmes : Aniss propose, Chouchou prend son temps.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers les deux bateaux.\n"
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
