#!/usr/bin/env python3
"""ATOM-AUT.ROU.001-07 — F-NAR-019. La flaque de Raphaël. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.ROU.001-07"
N1 = 10
TITLE = "La flaque de Raphaël"
FIL = (
    "Le zinc tape le mur. Sur le zinc, un éclat de gouttière brille. "
    "Raphaël veut la flaque, maintenant, en pyjama. Il enfonce une botte : "
    "elle glisse. Il prend les deux : elles se coincent. Il refuse de "
    "foncer, met le pull, boit, enfile une botte puis l'autre. Sous le "
    "zinc, l'éclat de gouttière tient sur l'eau."
)
CHARS = "Raphaël, papa, maman"
SETTING = "maison sous la pluie, gouttière, le matin"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "tout doucement",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
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
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "une chose, puis",
    "une chose puis",
    "grain de miette",
    "grain de sable",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de carotte",
    "grain de lavande",
    "éclat de pince",
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
    "éclat d'horloge",
    "éclat de tasse",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de orange",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de gouttière",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_flaque_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="bottes",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_pull_avant_les_bottes; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de gouttière",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_met_le_pull_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="flaque",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_sauter_des_deux_pieds; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de gouttière",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_eau; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}


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


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
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
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
        out.append(f"{role}|{ph}")
    return out


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


P0000 = [
    "narrateur|Le zinc de la gouttière tape le mur.",
    "narrateur|L'air sent la pluie, un peu froid.",
    "narrateur|La vitre est embuée, tiède sous le doigt.",
    "narrateur|Sur le zinc, un éclat de gouttière brille.",
    "enfant-m|Il est tout petit, papa.",
    "papa|C'est un éclat de gouttière.",
    "maman|Tu entends le zinc, Raphaël ?",
    "enfant-m|Oui, maman.",
    "narrateur|Le zinc chante, mince, contre le mur.",
    "narrateur|Un rond d'eau attend sous le zinc.",
    "enfant-m|Ma flaque !",
    "narrateur|En ce moment, Raphaël saute du lit.",
    "narrateur|Le pyjama bleu tombe sur ses genoux.",
    "narrateur|Les bottes vertes attendent près du tapis.",
    "enfant-m|Je mets les bottes, maintenant !",
    "narrateur|Il enfonce un pied dans une botte.",
    "narrateur|La botte est trop grande, trop lâche.",
    "narrateur|Elle glisse, tape le tapis.",
    "enfant-m|Elle glisse, papa !",
    "papa|Tes pieds sont dans le pyjama.",
    "narrateur|Il prend l'autre botte, d'un coup.",
    "narrateur|Les deux bottes se coincent.",
    "enfant-m|Ça ne veut pas !",
    "narrateur|Raphaël tire vers la porte.",
    "narrateur|Une botte reste collée au tapis.",
    "narrateur|Il trébuche, assis sur le pyjama.",
    "enfant-m|Oh.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|L'envie et l'inquiétude se bousculent.",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tu regardes tes pieds, Raphaël ?",
    "maman|Le pull attend sur la chaise.",
]

Q0001 = [
    "narrateur|Raphaël veut la flaque.",
    "narrateur|Que met-il avant les bottes ?",
]

C0001 = [
    "narrateur|Raphaël refuse de forcer l'autre botte.",
    "narrateur|Il retire le pied, sans tirer.",
    "narrateur|La botte verte reste sur le tapis.",
    "enfant-m|Je mets le pull.",
    "narrateur|Le pull bleu est sur la chaise.",
    "narrateur|Il enfile le pull, un peu rêche.",
    "enfant-m|C'est fait.",
    "maman|Tu viens au bol ?",
    "narrateur|Raphaël va vers la cuisine.",
    "narrateur|Le carrelage est froid sous les pieds.",
    "narrateur|Ça sent le lait, tiède.",
    "papa|Tu veux le bol vert ?",
    "enfant-m|Oui, le vert.",
    "narrateur|Il s'assoit, près de la table.",
    "narrateur|Une gorgée, puis une autre.",
    "enfant-m|Les bottes, maintenant !",
    "narrateur|Il saisit les deux bottes ensemble.",
    "narrateur|Elles se coincent, retombent.",
    "enfant-m|Oh.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Il ne reprend pas trop vite.",
    "narrateur|Il écoute le zinc, un instant.",
    "narrateur|Sur la vitre, l'éclat de gouttière brille.",
    "enfant-m|Il est là.",
    "narrateur|Raphaël refuse de foncer.",
    "narrateur|Il glisse un pied, puis l'autre.",
    "narrateur|Les bottes tiennent, fermes.",
    "papa|Merci, Raphaël.",
    "enfant-m|Elles restent.",
    "maman|On peut ouvrir ?",
    "enfant-m|Oui, pour la flaque.",
]

END = [
    "maman|J'ouvre la porte.",
    "narrateur|Maman pousse la porte, un peu.",
    "narrateur|L'air sent la pluie, frais.",
    "narrateur|Le zinc chante, mince, au-dessus.",
    "narrateur|Sous le zinc, une flaque ronde attend.",
    "enfant-m|Elle est là !",
    "papa|Tu poses un pied ?",
    "enfant-m|Les deux, maintenant !",
    "narrateur|Raphaël recule d'un pas.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Une botte entre dans l'eau.",
    "narrateur|Ça fait ploc.",
    "narrateur|Puis l'autre botte.",
    "narrateur|Ça fait ploc, plus large.",
    "enfant-m|C'est froid.",
    "maman|Tes pieds sont au chaud ?",
    "enfant-m|Oui, dans les bottes.",
    "narrateur|Un cercle d'eau s'ouvre.",
    "papa|On en fait un autre ?",
    "enfant-m|Oui.",
    "narrateur|Raphaël saute un tout petit peu.",
    "narrateur|L'eau saute aussi, claire.",
    "narrateur|Un rond de buée reste à la vitre.",
]

FIN = [
    "narrateur|Ils restent dans la flaque ronde.",
    "narrateur|L'eau touche le cuir des bottes.",
    "enfant-m|Ma flaque chante.",
    "maman|Oui, près de toi.",
    "narrateur|Sur l'eau, un éclat de gouttière brille.",
    "enfant-m|Comme sur le zinc, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, sur l'eau.",
    "narrateur|Raphaël recule le pied, sans se presser.",
    "narrateur|Le cuir repose dans le cercle.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est frais.",
    "narrateur|Le zinc repose contre le mur.",
    "narrateur|L'éclat de gouttière tient sur l'eau.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }]
    if missing:
        raise SystemExit(f"{SID} chunks inattendus: {missing}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "pluie,gouttiere",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "le pull",
                    "accepted_examples": (
                        "le pull | pull | le pull bleu | les vêtements "
                        "| d'abord le pull | avant les bottes | le pyjama non"
                    ),
                    "retry_prompt": "Le pull attend. Que met Raphaël avant les bottes ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "pull,bol",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "porte,flaque",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "zinc,eau",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de gouttière" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de gouttière" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "tout doucement" in blob:
        raise SystemExit(f"{SID}: tic tout doucement")
    if not all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks):
        raise SystemExit(f"{SID}: TTS incomplet")
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

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** AUT.ROU.001 — routine du matin (vécue : botte sur "
        "pyjama, pull puis bol puis bottes)\n"
        "- **Personnages :** Raphaël, papa, maman\n"
        "- **Lieu :** maison sous la pluie, gouttière, vitre embuée, le matin\n"
        "- **Indice unique :** éclat de gouttière (zinc → vitre → eau "
        "de la flaque)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le zinc tape le mur. L'air sent la pluie. Sur le zinc, un éclat de "
        "gouttière brille. Raphaël veut la flaque **maintenant**. Il enfonce "
        "une botte sur le pyjama : trop grande, elle glisse. Première idée : "
        "prendre les deux d'un coup, tirer vers la porte. Elles se coincent, "
        "il trébuche. Sourire parti. Papa s'accroupit. Raphaël refuse de "
        "forcer, met le pull, boit. Il saisit les deux bottes : elles "
        "retombent. Il écoute le zinc, voit l'éclat, refuse de foncer, "
        "enfile un pied puis l'autre. Merci vécu. À la flaque, il recule, "
        "pose une botte, ploc, puis l'autre. Sur l'eau, l'éclat tient.\n\n"
        "## Vécu\n\n"
        "Raphaël veut la flaque **maintenant**. Impatience, puis épaules "
        "qui tombent quand les bottes se coincent. Papa s'accroupit, pose "
        "une question, ne récite pas la règle. Raphaël agit : pull, bol, "
        "une botte puis l'autre. Merci vécu après les bottes fermes. Fin : "
        "l'éclat du début tient sur l'eau.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (zinc qui tape, éclat sur le zinc), pas "
        "« joue au salon », pas « Tout doucement ».\n"
        "- Monde du dump (maison sous la pluie, gouttière, le matin), "
        "distinct de ROU.001-01..006 (train, miettes, pain, fraises, "
        "bateau, doudou).\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout doucement » "
        "retirés. Pas de merle, pas de miel.\n"
        "- Leçon non dite : la flaque arrive quand le pull, le bol et les "
        "bottes tiennent. Pas de morale, pas « une chose puis l'autre ».\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de gouttière » nommé à l'ouverture, revu "
        "sur la vitre, payé sur l'eau.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        "- N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        f"- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
