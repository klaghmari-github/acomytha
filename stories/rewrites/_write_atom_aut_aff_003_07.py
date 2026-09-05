#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-07 — Le lapin et la soupe (F-NAR-019, N3, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-07"
TITLE = "Le lapin et la soupe"
N3 = LIMITS["N3"]
CHARS = "Amir, maman"
SETTING = "cuisine, parc, puis jardin"
FIL = (
    "Un toc sec vient du métal. Sur le bord, un éclat de casserole brille. "
    "Amir veut que le lapin voie le parc, maintenant, avant la soupe. "
    "Il pousse manteau et doudou dans le seau : trop lourd, ça bascule. "
    "Il refuse de forcer, reprend seau, manteau, lapin. Merci vécu. "
    "Au jardin, l'odeur de soupe appelle. Il refuse de foncer. "
    "Dans l'eau de la gourde, l'éclat pointe le lapin. Ils rentrent. "
    "L'éclat de casserole et le fil de vapeur se regardent."
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
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de carotte",
    "grain de pin",
    "grain de sable",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de liste",
    "éclat de caillou",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "point de gouttière",
    "point de gouttiere",
    "trait de vitre",
    "trait de craie",
    "peau d'orange",
    "peaux d'orange",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de casserole",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_parc_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="reprend",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; sous_texte=il_reprend_avant_de_partir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="seau",
        note=(
            "arc=confirmation; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=une_chose_puis_l_autre; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de casserole",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; sous_texte=il_refuse_de_foncer_vers_la_soupe; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de casserole",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_casserole_est_sur_le_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Il reprend ses affaires. Que fait Amir ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "casserole,vapeur",
        [
            "narrateur|Un toc sec vient du métal.",
            "narrateur|Le couvercle de la casserole repose de travers.",
            "narrateur|Le torchon sent le poireau, et la carotte.",
            "narrateur|La cuillère en bois laisse une trace humide.",
            "maman|La soupe attend pour ce soir, Amir.",
            "enfant-m|Ça sent bon.",
            "maman|Tu sens la carotte ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Et le poireau.",
            "narrateur|Maman pose le couvercle.",
            "narrateur|Ça fait un petit toc.",
            "narrateur|Un fil de vapeur glisse sur le bord.",
            "narrateur|Sur le bord, un éclat de casserole brille.",
            "enfant-m|Il brille, maman.",
            "maman|C'est un éclat de casserole, Amir.",
            "narrateur|Le doudou lapin attend sur la chaise.",
            "enfant-m|Le lapin veut le parc, maintenant !",
            "maman|La soupe reste ici.",
            "enfant-m|On y va ?",
            "maman|Oui, avec sa valise.",
            "narrateur|Ils ferment la porte de la cuisine.",
            "narrateur|La soupe reste à la maison.",
            "narrateur|En ce moment, Amir est au parc.",
            "narrateur|Le vent fraîchit sur le bac des valises.",
            "narrateur|Maman s'assoit sur le banc.",
            "narrateur|Amir a un seau rouge.",
            "narrateur|Son manteau vert attend sur le banc.",
            "narrateur|Le lapin attend dans l'herbe.",
            "enfant-m|Le seau, c'est sa valise.",
            "maman|Je te vois.",
            "narrateur|Amir verse le sable.",
            "narrateur|Ça fait chh.",
            "enfant-m|Il voyage, maman.",
            "maman|Le vent fraîchit.",
            "maman|On rentre.",
            "enfant-m|Le lapin n'a pas tout vu !",
            "enfant-m|Le jardin, maintenant !",
            "maman|Après, oui.",
            "narrateur|Amir veut tout mettre d'un coup.",
            "narrateur|Il pousse le manteau dans le seau.",
            "narrateur|Il pousse le lapin par-dessus.",
            "narrateur|Le seau bascule, trop lourd.",
            "narrateur|Le sable coule sur ses chaussures.",
            "enfant-m|Ça reste coincé !",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Tu reprends le seau ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Amir reprend le seau.",
            "narrateur|Avant de partir, que fait Amir ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "sable,banc",
        [
            "narrateur|Maman s'accroupit à la même hauteur.",
            "narrateur|Amir refuse de tirer plus fort.",
            "enfant-m|Je sors le lapin.",
            "narrateur|Il tire le tissu coincé, sans forcer.",
            "narrateur|Le lapin glisse, un peu froid.",
            "enfant-m|Il était dans le seau.",
            "maman|Tu le poses où ?",
            "enfant-m|Près du banc.",
            "narrateur|Amir pose le lapin sur le bois.",
            "narrateur|Le banc est froid sous la laine.",
            "maman|Et le manteau ?",
            "enfant-m|Je le prends.",
            "narrateur|Il reprend le manteau vert, sur le banc.",
            "narrateur|Le tissu vert gratte un peu, aux poignets.",
            "enfant-m|J'ai les bras dedans.",
            "maman|Tu as fini tes manches ?",
            "enfant-m|Oui, maman.",
            "narrateur|Amir reprend le seau près du bac.",
            "enfant-m|J'ai la valise.",
            "maman|Merci, Amir.",
            "narrateur|Maman ouvre le portillon du parc.",
            "narrateur|L'air frais pique les joues.",
            "enfant-m|On va au jardin ?",
            "maman|Oui, le lapin va le voir.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "herbe,gourde",
        [
            "narrateur|Plus tard, ils jouent au jardin.",
            "narrateur|L'odeur de soupe passe sous la porte.",
            "narrateur|Amir a une gourde.",
            "narrateur|Il a une casquette.",
            "narrateur|Le lapin est dans l'herbe courte.",
            "enfant-m|Je bois.",
            "maman|Doucement.",
            "narrateur|L'eau est fraîche.",
            "narrateur|Une feuille tourne près du pied.",
            "enfant-m|Le jardin, il a vu.",
            "enfant-m|La soupe, maintenant !",
            "maman|On rentre.",
            "enfant-m|Je cours !",
            "narrateur|Amir veut foncer vers la porte.",
            "narrateur|La gourde a roulé près de la feuille.",
            "narrateur|La casquette est sur une chaise basse.",
            "narrateur|Le sourire d'Amir se serre.",
            "narrateur|Ça serre, dans son ventre.",
            "enfant-m|Je n'aime pas ça.",
            "narrateur|Amir refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Amir observe la gourde, écoute le jardin.",
            "narrateur|Dans l'eau, un éclat blanc tremble.",
            "enfant-m|Comme l'éclat de casserole, maman !",
            "maman|Tu le vois, celui-là ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Il pointe le lapin.",
            "narrateur|Il contourne la feuille, lentement.",
            "narrateur|Il reprend la gourde près de la feuille.",
            "narrateur|Il reprend la casquette, sur la chaise.",
            "enfant-m|Et le lapin.",
            "narrateur|Le doudou est dans son bras.",
            "maman|Tu tiens le lapin ?",
            "enfant-m|Oui, il a voyagé.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "soupe,casserole",
        [
            "narrateur|Ils ouvrent la porte de la cuisine.",
            "narrateur|La soupe sent plus fort.",
            "maman|Tu poses la gourde près de l'évier ?",
            "narrateur|Amir pose la gourde.",
            "narrateur|Il pose la casquette.",
            "enfant-m|La soupe.",
            "maman|Oui, carotte et poireau.",
            "narrateur|Amir pose le lapin sur une chaise.",
            "enfant-m|Il a vu le parc.",
            "enfant-m|Il a vu le jardin.",
            "maman|Et maintenant, la soupe.",
            "narrateur|Un peu de vapeur monte.",
            "enfant-m|Mon éclat de casserole, maman.",
            "narrateur|Sur le bord, l'éclat de casserole brille.",
            "narrateur|Le fil de vapeur passe devant.",
            "enfant-m|Ils se regardent.",
            "maman|Tu les sens, la soupe et le lapin ?",
            "enfant-m|Oui, maman.",
            "enfant-m|La soupe sent le chaud.",
            "narrateur|L'éclat de casserole reste sur le bord.",
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
        extra_kw: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra_kw["pause_before_ms"] = 200
            extra_kw["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra_kw["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra_kw)
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
    opening = by["CHK_T0000_P0000"]["text"].lower()
    ending = by["CHK_T0000_P0000_END_F0001"]["text"].lower()
    if "éclat de casserole" not in opening:
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de casserole" not in ending:
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "reprend" not in opening:
        raise SystemExit(f"{SID}: reprendre absent à l'ouverture")
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
        "Un toc sec vient du métal. Le couvercle repose de travers. Sur le "
        "bord, un **éclat de casserole** brille. Amir veut que le lapin voie "
        "le parc, **maintenant**, avant la soupe. Au bac des valises, il "
        "pousse manteau et doudou dans le seau d'un coup : trop lourd, ça "
        "bascule. Première idée ratée. Maman s'accroupit. Il refuse de "
        "forcer, sort le lapin, reprend le manteau, reprend le seau. Merci "
        "vécu. Au jardin, l'odeur de soupe passe sous la porte. Il veut "
        "courir : gourde et casquette restent. Il refuse de foncer. Dans "
        "l'eau, un éclat blanc tremble, comme sur la casserole, et pointe "
        "le lapin. Ils rentrent. L'éclat de casserole et le fil de vapeur "
        "se regardent.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine (casserole, torchon, carotte, poireau), parc "
        "(bac des valises, banc, seau-valise), jardin (chaises basses, "
        "gourde, feuille).\n"
        "- Désir : porter le lapin jusqu'au parc, puis au jardin, avant "
        "la soupe.\n"
        "- Objet : seau rouge, manteau vert, doudou lapin, gourde, casquette.\n"
        "- Indice unique : éclat de casserole, vu dès l'ouverture, payé "
        "dans l'eau de la gourde puis sur le bord.\n"
        "- Urgence douce : la soupe attend, l'odeur passe sous la porte.\n"
        "- Imprévu 1 : tout d'un coup, seau trop lourd, sable sur les "
        "chaussures, lapin coincé.\n"
        "- Cue : maman à la même hauteur, une chose puis l'autre. Un "
        "merci vécu, après le seau repris.\n"
        "- Imprévu 2 (plus rusé) : il veut courir vers la soupe ; gourde "
        "et casquette restent ; l'éclat dans l'eau désigne le lapin.\n"
        "- Résolution : il refuse de foncer, contourne, reprend.\n"
        "- Retour : cuisine, lapin sur la chaise, éclat de casserole "
        "face au fil de vapeur.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.003 (reprendre ses affaires avant de partir) "
        "greffée, jamais dite. La première idée (tout d'un coup) échoue. "
        "Le choix d'Amir change l'action. Un « en ce moment ». Un merci "
        "vécu. Adulte + question. Troupe D16 : Amir, maman.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : cuisine, parc, puis "
        "jardin. ≠ 003-01 parc/seau jaune, ≠ 003-02 cuisine orange/"
        "maison du lapin, ≠ 003-03 ours capitaine/pique-nique, ≠ 003-04 "
        "chaussettes/square, ≠ 003-05 feuille/aire de jeux, ≠ 003-06 "
        "gouttière/seau vert.\n"
        "- Ouverture inventée (toc du métal, couvercle de travers), pas "
        "un gabarit v2.\n"
        "- Indice unique : éclat de casserole. Pas grain de sable/"
        "miette/foin/feuille/paille/toile/pépin/pomme/carotte/pin, pas "
        "éclat de pince/thermos/coquille/bouton/ticket/goutte/boucle/"
        "corde/caisse/marche/clé/cuillère/sonnette/horloge/liste/caillou/"
        "tasse/orange/colle/lessive/vitre, pas point de gouttière, merle, "
        "miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (reprendre). 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
