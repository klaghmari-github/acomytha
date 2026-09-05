#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-04 — Le bateau de Mila (F-NAR-019, N2, AUT.AFF.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-04"
TITLE = "Le bateau de Mila"
N2 = LIMITS["N2"]
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
    "grain de miette",
    "grain de foin",
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de corde",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=le_bateau_tape_sous_le_plancher; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sac",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=les_affaires_vont_dans_le_sac; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="dessin",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; intensite=1; "
            "destinataire=enfant; sous_texte=une_chose_puis_la_suivante; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de corde",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_refuse_de_foncer_l_éclat_dit_le_vent; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de corde",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_éclat_porte_une_trace_de_sel; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "le sac",
    "accepted_examples": "le sac | dans le sac | il met | elle met | mettre",
    "retry_prompt": "Elle met les affaires dans le sac. Où les met Mila ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "eau-port,corde,plancher",
        [
            "narrateur|Sous le plancher, le bois du quai tape.",
            "narrateur|Le son grimpe l'escalier, puis la pièce.",
            "narrateur|Dans l'appartement, ça sent le savon et le sel.",
            "narrateur|Une mouette crie contre la vitre.",
            "narrateur|Sur le rebord, un éclat de corde brille.",
            "narrateur|Il est pâle, raide, et il sent le sel.",
            "narrateur|Le vent du port l'a posé là.",
            "narrateur|Mila ne sait pas à quoi il servira.",
            "narrateur|Son dessin du bateau sèche sur la table.",
            "narrateur|La peinture jaune luit, un peu collante.",
            "narrateur|En bas, le vrai bateau bleu frappe le quai.",
            "enfant-f|Je veux le bateau, maintenant !",
            "maman|Mila, tu entends l'eau ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Il m'attend.",
            "maman|On y va, avec le sac.",
            "narrateur|En ce moment, Mila saisit le sac bleu.",
            "narrateur|Le tissu gratte sous ses doigts.",
            "narrateur|La sangle sent le sel, comme la corde.",
            "maman|Prends de l'eau, pour le quai.",
            "narrateur|Mila prend la gourde froide.",
            "narrateur|Le goûter sent la pomme, dans son papier.",
            "enfant-f|Je mets tout, d'un coup !",
            "narrateur|Elle pousse gourde, pomme et dessin.",
            "narrateur|Le zip mord le papier du dessin.",
            "narrateur|Le bateau jaune se plie, de travers.",
            "enfant-f|Ça reste coincé !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila prépare le sac.",
            "narrateur|Où met-elle les affaires ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "zip,tissu",
        [
            "narrateur|Maman s'accroupit à la même hauteur.",
            "maman|Sors le dessin, d'abord.",
            "narrateur|Mila tire le papier coincé.",
            "narrateur|Le zip lâche, petit à petit.",
            "narrateur|Elle pose le dessin à plat, sur la table.",
            "maman|L'eau va au fond.",
            "narrateur|Mila range la gourde froide.",
            "narrateur|Le papier de la pomme glisse à côté.",
            "enfant-f|Et mon doudou ?",
            "narrateur|Le doudou n'est pas près des chaussures.",
            "maman|Regarde dans la poche du manteau.",
            "narrateur|Mila cherche dans la poche.",
            "narrateur|Le doudou sent le coton chaud.",
            "enfant-f|Il était caché.",
            "narrateur|Elle le glisse dans le sac.",
            "narrateur|Le zip avance, sans mordre.",
            "enfant-f|Il part.",
            "maman|Le sac est prêt ?",
            "enfant-f|Pas le dessin.",
            "narrateur|Le bateau jaune attend sur la table.",
            "maman|Tu prends aussi ton dessin ?",
            "enfant-f|Oui, pour le vrai bateau.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "vent,fenetre,marches",
        [
            "narrateur|Un souffle entre par la fenêtre.",
            "narrateur|Le dessin glisse vers le rebord.",
            "enfant-f|Il va tomber !",
            "narrateur|Mila veut courir, le papier à la main.",
            "narrateur|Elle veut descendre, sans le sac.",
            "narrateur|Mila refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Sur le rebord, l'éclat de corde tremble.",
            "narrateur|Il penche vers la fenêtre ouverte.",
            "enfant-f|C'est le vent !",
            "maman|Le vent vient d'où ?",
            "enfant-f|De là, du quai.",
            "narrateur|Mila pousse la fenêtre.",
            "narrateur|Le dessin s'arrête, à plat.",
            "narrateur|Elle glisse l'éclat de corde dans le sac.",
            "narrateur|Puis le dessin, à la fin.",
            "narrateur|Le zip glisse jusqu'au bout.",
            "maman|Merci, Mila.",
            "maman|On va vers le quai ?",
            "enfant-f|Oui, le dessin est dans le sac.",
            "narrateur|Mila passe la sangle sur l'épaule.",
            "narrateur|Elles descendent les marches du port.",
            "narrateur|L'air sent le sel et le bois mouillé.",
            "narrateur|Une corde mouillée frappe un anneau.",
            "narrateur|Le bateau bleu tape l'eau.",
            "enfant-f|Il est là.",
            "maman|Oui, il est près.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "bois,eau,sel",
        [
            "narrateur|Mila pose le pied sur le bois du bateau.",
            "narrateur|Le bateau bouge, léger.",
            "enfant-f|On flotte, maman.",
            "maman|Oui, tu es arrivée.",
            "narrateur|Le sac bleu voyage contre sa hanche.",
            "narrateur|Mila ouvre le sac.",
            "narrateur|L'éclat de corde porte une trace de sel.",
            "narrateur|Le dessin jaune reste plat.",
            "enfant-f|Il a voyagé.",
            "maman|Comme toi.",
            "narrateur|Le sel pique un peu les lèvres.",
            "narrateur|L'eau du port tape le bois du bateau.",
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
        extra: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra["pause_before_ms"] = 200
            extra["fields"] = Q_FIELDS
        by[cid] = voice(c, lines, profile, sons, extra)
    merged = dict(src)
    merged["fil_rouge"] = (
        "Sous le plancher, le bois du quai tape. Un éclat de corde pâle "
        "brille sur le rebord. Mila veut porter son dessin jusqu'au bateau "
        "bleu, maintenant. Elle pousse tout dans le sac : le zip mord, le "
        "bateau jaune se plie. Maman s'accroupit. Une chose, puis la "
        "suivante. Un souffle glisse le dessin vers la fenêtre. Mila refuse "
        "de foncer. L'éclat de corde penche : c'est le vent. Elle ferme, "
        "glisse l'éclat, puis le dessin. Sur le bois du bateau, l'éclat "
        "porte une trace de sel."
    )
    merged["title"] = TITLE
    merged["characters"] = "Mila, maman"
    merged["setting"] = "appartement au-dessus du quai puis bateau du port"
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in merged["chunks"]
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if "éclat de corde" not in " ".join(c["text"] for c in merged["chunks"]):
        raise SystemExit("indice éclat de corde absent")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "Le bois du quai tape sous le plancher de l'appartement. Un éclat de "
        "corde pâle, raide, sent le sel sur le rebord. Mila veut porter son "
        "dessin jaune jusqu'au bateau bleu, maintenant. Elle pousse tout dans "
        "le sac d'un coup : le zip mord, le bateau se plie. Maman s'accroupit. "
        "Une chose, puis la suivante. Un souffle glisse le dessin vers la "
        "fenêtre. Mila refuse de foncer. L'éclat penche : c'est le vent. Elle "
        "ferme, glisse l'éclat, puis le dessin. Sur le bois du bateau, "
        "l'éclat porte une trace de sel.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : appartement au-dessus du quai, savon et sel, mouette, "
        "rebord, bateau bleu en bas.\n"
        "- Désir : porter le dessin jusqu'au vrai bateau, maintenant.\n"
        "- Objet : sac bleu, dessin jaune, gourde, pomme, doudou.\n"
        "- Indice unique : éclat de corde, vu dès l'ouverture, payé au climax "
        "et sur le bateau.\n"
        "- Urgence douce : le bateau tape, le vent peut prendre le dessin.\n"
        "- Imprévu 1 : tout d'un coup, zip qui mord, dessin plié.\n"
        "- Cue : maman à la même hauteur, une chose puis la suivante. "
        "Un merci vécu, après le dessin rangé.\n"
        "- Imprévu 2 (plus rusé) : le souffle vers la fenêtre ; Mila veut "
        "descendre sans le sac.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, ferme, glisse "
        "l'éclat puis le dessin. Une corde mouillée frappe un anneau au quai.\n"
        "- Retour : pied sur le bois, on flotte, l'éclat a une trace de sel, "
        "le dessin reste plat.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.001 (préparer le sac) greffée, jamais dite. La première "
        "idée (tout d'un coup) échoue. Le choix de Mila change l'action. "
        "Un « en ce moment ». Un merci vécu. Adulte + question. Troupe D16 : "
        "Mila, maman.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : appartement au-dessus du quai puis "
        "bateau du port. ≠ four, ≠ cour, ≠ pente, ≠ bateau sur la vitre.\n"
        "- Ouverture inventée (le son grimpe le plancher), pas un gabarit v2.\n"
        "- Indice unique : éclat de corde. Pas grain de miette/foin/paille/"
        "toile/pépin, pas éclat de pince/thermos/coquille/bouton/ticket/"
        "goutte/boucle, pas trait de craie, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (le sac). 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
