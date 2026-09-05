#!/usr/bin/env python3
"""ATOM-AUT.ROU.001-05 — Le bateau d'Amir (F-NAR-019, N3, AUT.ROU.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.ROU.001-05"
TITLE = "Le bateau d'Amir"
N3 = LIMITS["N3"]
INDICE = "éclat de quille"
CHARS = "Amir, papa, maman"
SETTING = "chambre, cuisine, jardin, arrosoir sur le bassin, le matin"
FIL = (
    "Dans le jardin, l'arrosoir tape le bassin vide. Sur la noix, un éclat "
    "de quille luit. Amir veut flotter maintenant. Il prend tout : la feuille "
    "s'envole, la noix glisse, l'éclat disparaît. Papa s'accroupit. Merci "
    "vécu. Il refuse de foncer. Sur l'eau, l'éclat de quille reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de sable",
    "grain de toile",
    "grain de laine",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de carreau",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de sonnette",
    "éclat de liste",
    "éclat de clé",
    "éclat de cuillère",
    "éclat de tasse",
    "éclat d'orange",
    "éclat d'écorce",
    "éclat de wagon",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de lampe",
    "éclat de citron",
    "éclat de promenade",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de quille",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_noix_sur_l_eau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="bassin",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_se_prepare_une_chose_apres_l_autre; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="éclat de quille",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_feuille_d_abord_puis_la_noix_sous_le_lit; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de quille",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de quille",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_eau; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "une chose",
    "accepted_examples": (
        "une chose | puis l'autre | d'abord | doucement | "
        "une chose puis l'autre | puis la suivante"
    ),
    "retry_prompt": "Il fait une chose, puis la suivante. Comment se prépare Amir ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "rayon,arrosoir",
        [
            "narrateur|Dans le jardin, l'arrosoir tape le bassin.",
            "narrateur|Le métal est froid, un peu creux.",
            "narrateur|Dans la chambre, une feuille sèche cliquette.",
            "narrateur|Elle est posée près d'une noix ridée.",
            "narrateur|Un éclat de quille luit sur son dos.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur le bois de la noix ?",
            "narrateur|Deux pantoufles allongent des quais jaunes.",
            "narrateur|Un rayon les touche, près du tapis crème.",
            "narrateur|La poussière danse dans le rayon.",
            "maman|Le bassin du jardin attend de l'eau.",
            "narrateur|L'air sent la banane, depuis la cuisine.",
            "maman|J'ai coupé un fruit, Amir.",
            "enfant-m|Mon bateau va flotter, maintenant !",
            "papa|Ta noix veut l'eau, Amir.",
            "narrateur|En ce moment, Amir saisit noix et feuille.",
            "narrateur|Il glisse les pieds dans les pantoufles.",
            "narrateur|Il marche vers la porte, en pyjama.",
            "enfant-m|On va à l'eau !",
            "narrateur|La feuille s'envole derrière la chaise.",
            "narrateur|La noix bascule, et l'éclat de quille disparaît.",
            "enfant-m|Oh !",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dehors, le bassin est vide, gris.",
            "enfant-m|Il n'y a pas d'eau.",
            "papa|L'eau n'est pas versée.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Je prends tout, et j'y vais !",
            "narrateur|Il ramasse noix, feuille, pantoufles d'un coup.",
            "narrateur|La noix glisse, clac, sous le lit.",
            "narrateur|L'éclat de quille s'est caché.",
            "enfant-m|Il est perdu.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Amir veut le bassin.",
            "narrateur|Comment se prépare-t-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "banane,lait",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu regardes bien sous le lit ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir pose la feuille sur la table.",
            "narrateur|Puis il cherche, une main, près du tapis.",
            "narrateur|Ses doigts trouvent la noix froide.",
            "enfant-m|Ma noix !",
            "narrateur|Un éclat de quille reparaît, pâle.",
            "papa|Merci, tu l'as trouvée.",
            "enfant-m|Elle était dessous.",
            "maman|Le pull rouge, sur le dossier.",
            "narrateur|Amir enfile le pull.",
            "narrateur|Le pull est rêche aux poignets.",
            "enfant-m|Je suis habillé.",
            "maman|La cuisine, maintenant.",
            "narrateur|Ça sent la banane et le lait tiède.",
            "maman|Tu veux la banane coupée ?",
            "enfant-m|Oui, maman.",
            "narrateur|Amir s'assoit à table.",
            "narrateur|La banane est douce, un peu sucrée.",
            "papa|Dehors, je verse l'eau.",
            "papa|Tu finis ton bol, et l'eau sera prête.",
            "enfant-m|D'accord.",
            "narrateur|Il boit une gorgée de lait.",
            "narrateur|Le lait est tiède contre la lèvre.",
            "maman|Ensuite, le sac.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "porte",
        [
            "narrateur|Amir met la gourde dans le sac.",
            "narrateur|Il glisse le cahier à côté.",
            "narrateur|Il pose la noix tout au-dessus.",
            "enfant-m|La feuille aussi.",
            "papa|Tu as mis le bateau ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir range les pantoufles près du tapis.",
            "maman|Tu les as remises au quai ?",
            "enfant-m|Oui.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|L'air sent le jardin, un peu humide.",
            "narrateur|Le bassin a un peu d'eau, grise.",
            "enfant-m|Je jette tout, maintenant !",
            "narrateur|Il avance les mains vers le sac.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Il refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Amir observe la noix, écoute le jardin.",
            "narrateur|Sur le dos, l'éclat de quille luit.",
            "enfant-m|Là, près de l'éclat.",
            "narrateur|Il pose d'abord les pantoufles au bord.",
            "narrateur|Deux petits quais, comme dans la chambre.",
            "narrateur|Puis la noix, au creux de l'eau.",
            "enfant-m|La feuille-voile, maintenant.",
            "papa|Tu souffles, ou je souffle ?",
            "enfant-m|Toi, papa.",
            "narrateur|Papa souffle.",
            "narrateur|La noix avance, lente, sur l'eau.",
            "maman|Elle flotte.",
            "narrateur|Un petit rond d'eau s'ouvre.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "eau",
        [
            "enfant-m|Le bateau est parti.",
            "narrateur|Maman s'assoit au bord du bassin.",
            "papa|Tu veux un bout de banane ?",
            "enfant-m|Oui, papa.",
            "narrateur|La banane sent fort, sucrée.",
            "enfant-m|La noix a un petit éclat.",
            "narrateur|Un éclat de quille tient sur l'eau.",
            "maman|Tu le vois, comme sur la table ?",
            "enfant-m|Oui, maman.",
            "narrateur|L'arrosoir se tait, dehors.",
            "narrateur|Sur l'eau, l'éclat de quille reste pâle.",
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
        elif cid != "CHK_T0000_P0000":
            extra["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra)
    merged = dict(src)
    merged["fil_rouge"] = FIL
    merged["title"] = TITLE
    merged["characters"] = CHARS
    merged["setting"] = SETTING
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    blob = "\n".join(c["script"] for c in merged["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "il refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")
    merci_n = sum(
        1
        for ln in blob.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
        if "merci" in ln or "bravo" in ln
    )
    if merci_n != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{merci_n}")
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
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "Dans le jardin, l'arrosoir tape le bassin vide. Dans la chambre, "
        "une feuille sèche cliquette près d'une noix ridée. Un éclat de "
        "quille luit sur son dos. Amir veut le bateau sur l'eau, "
        "**maintenant**. Il saisit tout, en pyjama : la feuille s'envole, "
        "la noix bascule, l'éclat disparaît. Le bassin est vide. Il ramasse "
        "d'un coup : clac, la noix glisse sous le lit. Papa s'accroupit. "
        "La feuille d'abord, puis la noix. Merci vécu, quand l'éclat "
        "reparaît. Au bord de l'eau, il veut tout jeter. Il refuse de "
        "foncer, lit l'éclat. Sur l'eau, l'éclat de quille reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, cuisine, jardin, arrosoir, bassin, le matin. "
        "≠ train de l'allée, ≠ miettes d'oiseau, ≠ pain chaud, ≠ fraises "
        "du marché.\n"
        "- Désir : porter la noix-bateau jusqu'à l'eau, maintenant.\n"
        "- Objet : noix ridée, feuille-voile, pantoufles-quais, arrosoir.\n"
        "- Indice unique : éclat de quille, vu dès l'ouverture, payé sur "
        "l'eau.\n"
        "- Urgence douce : le bassin attend, l'arrosoir tape.\n"
        "- Imprévu 1 : tout d'un coup, pyjama, feuille perdue, noix sous "
        "le lit, bassin vide.\n"
        "- Cue : papa à la même hauteur. Feuille posée, puis la noix. Un "
        "merci vécu, après l'éclat pâle.\n"
        "- Imprévu 2 (plus rusé) : tout jeter dans l'eau d'un coup.\n"
        "- Résolution : il refuse de foncer, lit l'éclat, quais puis noix "
        "puis voile.\n"
        "- Retour : banane, arrosoir silencieux, éclat de quille pâle sur "
        "l'eau.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.ROU.001 (une chose, puis la suivante, jamais dite) "
        "greffée. La première idée (tout d'un coup) échoue. Le choix "
        "d'Amir change l'action. Un « en ce moment ». Un merci vécu. "
        "Adulte + question. Troupe D16 : Amir, papa, maman.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : chambre, cuisine, jardin, "
        "le matin. Sans lumière de miel. ≠ ROU.001-01..004.\n"
        "- Ouverture inventée (arrosoir qui tape le bassin), pas un "
        "gabarit v2.\n"
        "- Indice unique : éclat de quille. Pas merle-trois-notes, miel, "
        "gouttes, pas tache/flèche/marque/symbole, pas éclat de wagon/"
        "bec/marche/fraise.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (une chose). 5 chunks, kinds "
        "inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
