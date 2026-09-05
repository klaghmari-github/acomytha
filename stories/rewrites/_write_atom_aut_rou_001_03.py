#!/usr/bin/env python3
"""ATOM-AUT.ROU.001-03 — Le pain chaud de Nino (F-NAR-019, N1, AUT.ROU.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.ROU.001-03"
TITLE = "Le pain chaud de Nino"
N1 = LIMITS["N1"]
CHARS = "Nino, papa, maman"
SETTING = "chambre, escalier, cuisine, le matin"
FIL = (
    "En bas, un plat se pose. Toc. Sur la première marche, un éclat de "
    "marche brille. Nino veut le pain chaud maintenant. Il court en "
    "pyjama : le pied glisse. Il refuse de foncer, met le pull jaune, "
    "ramasse la chaussette. L'éclat de marche guide. Sur la croûte, "
    "l'éclat garde une trace."
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
    "une chose, puis",
    "une étape",
    "grain de vanille",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de sable",
    "éclat de farine",
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
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de lampe",
    "éclat de citron",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "marque fine",
    "ombre en forme",
    "train de l'allée",
    "train de l'allee",
    "oiseau gris",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de marche",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_pain_chaud_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="pain",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_se_prepare_une_chose_apres_l_autre; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de marche",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="pain",
        note=(
            "arc=action; intention=refermer_le_désir; "
            "emotion=fierté_calme et chaleur; intensite=2; "
            "destinataire=enfant; sous_texte=le_pain_arrive_jusqu_a_lui; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de marche",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_la_marche_est_sur_la_croute; "
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
    "retry_prompt": "Il fait une chose, puis la suivante. Comment se prépare Nino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pain,vapeur",
        [
            "narrateur|En bas, un plat se pose.",
            "narrateur|Toc.",
            "narrateur|Une vapeur grimpe l'escalier.",
            "narrateur|Elle sent le beurre.",
            "narrateur|Ça sent la croûte dorée.",
            "narrateur|Sur la première marche, un éclat de marche brille.",
            "enfant-m|Il est blanc, maman.",
            "maman|C'est la vapeur du pain.",
            "narrateur|L'éclat de marche tient comme une petite lune.",
            "narrateur|Les marches de bois sont lisses.",
            "narrateur|La rampe est ronde sous la main.",
            "narrateur|Un carré de soleil touche le bois.",
            "narrateur|La chambre sent le pain, tiède.",
            "papa|Nino, tu sens le pain ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Je le veux, maintenant.",
            "papa|Il est sur la planche, en bas.",
            "narrateur|Le pull jaune attend près du lit.",
            "narrateur|En ce moment, Nino est dans son lit.",
            "narrateur|L'oreiller est plat.",
            "narrateur|Le drap sent le sommeil.",
            "enfant-m|Plus tard, le pull.",
            "narrateur|Nino pose un pied par terre.",
            "narrateur|Le tapis est chaud sous les orteils.",
            "narrateur|Il court vers l'escalier, en pyjama.",
            "narrateur|Sa main rate la rampe.",
            "narrateur|Son pied glisse sur l'éclat de marche.",
            "enfant-m|Oh.",
            "narrateur|Il s'assoit d'un coup, sur la marche.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Le pain part ?",
            "maman|Non.",
            "maman|Il reste au chaud.",
            "narrateur|Nino veut redescendre d'un seul élan.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu regardes la marche ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino veut le pain.",
            "narrateur|Comment se prépare-t-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pull,marches",
        [
            "narrateur|Nino revient vers le lit.",
            "narrateur|Ses pieds touchent le tapis.",
            "narrateur|Le pull jaune est près du lit.",
            "enfant-m|Toi d'abord.",
            "narrateur|Il enfile le pull.",
            "narrateur|Le pull est doux sur les bras.",
            "narrateur|Le pyjama reste en dessous, chaud.",
            "enfant-m|C'est fait.",
            "maman|Tu vas vers les marches ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino s'arrête devant la première marche.",
            "narrateur|L'éclat de marche brille, petit.",
            "enfant-m|Je te vois.",
            "narrateur|Sa main trouve la rampe.",
            "narrateur|La rampe est ronde, un peu froide.",
            "narrateur|Une marche, sous le pied.",
            "narrateur|Puis une autre.",
            "enfant-m|Je regarde.",
            "narrateur|Au milieu, une chaussette traîne.",
            "enfant-m|Je la pousse.",
            "narrateur|Nino lève le pied, trop vite.",
            "narrateur|Puis il s'arrête.",
            "enfant-m|Attends.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il ramasse la chaussette.",
            "narrateur|Sous le tissu, l'éclat de marche brille.",
            "enfant-m|Comme en haut !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, près du bois.",
            "narrateur|Nino glisse la chaussette dans sa main.",
            "narrateur|Il descend, sans sauter.",
            "narrateur|La cuisine est chaude.",
            "narrateur|Le pain est sur la planche.",
            "papa|Merci, tu as regardé.",
            "maman|Te voilà.",
            "enfant-m|Il est chaud.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pain,beurre",
        [
            "papa|Tu t'assois ?",
            "narrateur|Nino s'assoit à table.",
            "maman|Un peu de beurre ?",
            "enfant-m|Oui, un peu.",
            "narrateur|Le beurre fond sur la croûte.",
            "narrateur|Nino mord la croûte.",
            "narrateur|Le pain est tiède.",
            "enfant-m|C'est bon.",
            "papa|Tu as une miette ici.",
            "narrateur|Papa montre le menton.",
            "enfant-m|Je l'essuie.",
            "maman|On le mange ici.",
            "enfant-m|Oui, ici.",
            "narrateur|Nino lève les yeux vers l'escalier.",
            "narrateur|Sur la première marche, l'éclat de marche brille.",
            "enfant-m|Il est là, papa.",
            "papa|Comme tout à l'heure.",
            "narrateur|La chaleur touche les joues de Nino.",
            "maman|On est bien, ici.",
            "enfant-m|Le pain est venu.",
            "narrateur|La rampe de bois reste tiède.",
            "narrateur|Nino sent le beurre sur ses doigts.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pain",
        [
            "enfant-m|Le pain était chaud.",
            "maman|Tu es venu jusqu'à lui.",
            "narrateur|Une petite vapeur flotte, blanche.",
            "narrateur|Nino sent le beurre sur sa langue.",
            "narrateur|Sur la croûte, l'éclat de marche garde une trace.",
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
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if blob.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{blob.count('merci')}")
    if "éclat de marche" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de marche" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
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
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** AUT.ROU.001 — enchaîner le matin (vécue, jamais dite)\n"
        "- **Personnages :** Nino, papa, maman. Troupe D16.\n"
        "- **Lieu :** chambre, escalier, cuisine, le matin. ≠ ROU-001-01 "
        "train de l'allée. ≠ ROU-001-02 miettes Victorina. ≠ RAN-001-03 "
        "pain d'Amir (éclat de farine, couloir).\n"
        "- **Indice unique :** éclat de marche (première marche → sous la "
        "chaussette → regard vers l'escalier → trace sur la croûte)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "En bas, un plat se pose. Toc. Une vapeur grimpe. Sur la première "
        "marche, un éclat de marche brille. Nino veut le pain chaud "
        "**maintenant**. Le pull jaune attend. Il dit plus tard, court en "
        "pyjama. La main rate la rampe. Le pied glisse sur l'éclat. Première "
        "idée ratée. Sourire disparu. Papa se baisse. Il refuse de foncer, "
        "met le pull, pose la main, descend. Une chaussette cache l'éclat : "
        "il veut la pousser, s'arrête, ramasse. L'éclat est dessous. Merci "
        "vécu. À table, la croûte craque. L'éclat de marche garde une trace "
        "sur la croûte.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, escalier de bois, rampe ronde, cuisine, vapeur, "
        "beurre, matin.\n"
        "- Désir : le pain chaud sur la planche, maintenant.\n"
        "- Objet : pain, pull jaune, rampe, chaussette.\n"
        "- Indice unique : éclat de marche, vu dès l'ouverture, payé au "
        "climax et sur la croûte.\n"
        "- Urgence douce : le pain est chaud, la vapeur grimpe.\n"
        "- Imprévu 1 : il saute le pull, court en pyjama ; le pied glisse "
        "sur l'éclat ; redescendre d'un élan échoue.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, après "
        "la descente regardée.\n"
        "- Imprévu 2 (plus rusé) : une chaussette cache l'éclat au milieu "
        "des marches ; il veut la pousser d'un coup.\n"
        "- Résolution : il refuse de foncer, ramasse, lit l'éclat, descend "
        "sans sauter. Le pain est là.\n"
        "- Retour : croûte, beurre, regard vers la marche, éclat en trace "
        "sur la croûte. Pas de liste sac-chaussures-porte.\n\n"
        "## Vécu\n\n"
        "Nino veut le pain **maintenant**. Impatience (course en pyjama), "
        "puis sourire qui disparaît, épaules qui tombent. Papa se baisse, "
        "pose une question, ne récite pas la règle. Nino agit : pull, rampe, "
        "chaussette ramassée, marches regardées. Merci vécu après la "
        "descente. Leçon greffée : le pain n'arrive que quand une chose "
        "suit l'autre. Fin : l'éclat du début est sur la croûte. Toc n'est "
        "pas le merle à trois notes.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : chambre, escalier, cuisine, "
        "le matin. ≠ train, ≠ miettes, ≠ éclat de farine, ≠ fournil.\n"
        "- Ouverture inventée (plat Toc, vapeur, éclat), pas un gabarit v2, "
        "pas « Nino est dans l'entrée ».\n"
        "- Indice unique : éclat de marche (roster). Pas grain de vanille/"
        "miette/foin/feuille/paille/pin/pépin/pomme/sable, pas éclat de "
        "pince/thermos/coquille/bouton/ticket/goutte/boucle/corde/caisse/"
        "caillou/liste/clé/cuillère/sonnette/horloge/tasse/orange/colle/"
        "lessive/vitre/casserole/carreau/grain/nappe/boîte/wagon/bec/"
        "fraise/quille/promenade/lampe/citron/farine, pas pli de voile, "
        "point de gouttière, trait de craie/vitre, merle, miel, marque "
        "fine, ombre-flèche.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : il enfile, il regarde, il descend. Pas "
        "« une chose, puis la suivante » en refrain. Pas de liste bannie "
        "(sac, chaussures, porte).\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (une chose). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive à table.\n"
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
