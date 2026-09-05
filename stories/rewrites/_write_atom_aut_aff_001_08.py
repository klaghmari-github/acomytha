#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-08 — Le château de la rive (F-NAR-019, N2, AUT.AFF.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-08"
TITLE = "Le château de la rive"
N2 = LIMITS["N2"]
INDICE = "éclat de caillou"
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
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de caillou",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse; intensite=2; destinataire=enfant; "
            "sous_texte=elle_veut_le_chateau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sac",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=les_affaires_vont_dans_le_sac; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="éclat de caillou",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=une_chose_puis_la_suivante; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="sac",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sans_le_sac; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de caillou",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_dessin_est_la_fenetre_du_mur; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "le sac",
    "accepted_examples": "le sac | dans le sac | il met | elle met | mettre",
    "retry_prompt": "Elle met les affaires dans le sac. Où les met Victorina ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin,dalle,arrosoir",
        [
            "narrateur|Sur la table du jardin, la poussière est tiède.",
            "narrateur|Victorina dessine un château, du doigt.",
            "narrateur|Le doigt bute contre un éclat de caillou.",
            "narrateur|Le petit morceau luit, pâle.",
            "enfant-f|Il brille, papa.",
            "papa|C'est un morceau du chemin.",
            "narrateur|Elle le pose au milieu du dessin.",
            "enfant-f|C'est ma fenêtre.",
            "narrateur|Derrière la haie, le fleuve clapote.",
            "narrateur|L'air sent l'herbe coupée et l'eau.",
            "narrateur|Les bottes attendent près de l'arrosoir.",
            "maman|Victorina, on va à la rive.",
            "enfant-f|Je veux mon château, maintenant !",
            "maman|Avec le seau, et le sac.",
            "narrateur|Le seau rouge attend près des bottes.",
            "narrateur|En ce moment, Victorina saisit le sac.",
            "narrateur|Le tissu gratte sous ses doigts.",
            "papa|Prends de l'eau, la rive est au soleil.",
            "narrateur|Victorina prend la gourde froide.",
            "narrateur|Le bouchon fait un petit clic.",
            "enfant-f|Je mets tout, d'un coup !",
            "narrateur|Elle pousse gourde, seau et pelle.",
            "narrateur|Le zip mord le manche de la pelle.",
            "narrateur|Le seau bascule, tape la dalle.",
            "narrateur|L'éclat de caillou roule sous le banc.",
            "enfant-f|Ça reste coincé !",
            "narrateur|Le sourire de Victorina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina prépare le sac.",
            "narrateur|Où met-elle les affaires ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "zip,sac",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Sors la pelle, d'abord.",
            "narrateur|Victorina tire le manche coincé.",
            "narrateur|Le zip lâche, petit à petit.",
            "maman|L'eau va au fond.",
            "narrateur|Elle range la gourde froide.",
            "narrateur|Le seau rouge glisse à côté.",
            "enfant-f|Et mon éclat ?",
            "narrateur|L'éclat de caillou n'est pas sur la dalle.",
            "papa|Regarde sous le banc ?",
            "narrateur|Victorina se baisse près du bois.",
            "narrateur|Ses doigts trouvent le bord lisse.",
            "enfant-f|Il était caché.",
            "narrateur|Elle le glisse dans la poche du sac.",
            "narrateur|Le zip avance, sans mordre.",
            "papa|Merci, Victorina.",
            "enfant-f|Il part.",
            "papa|Le sac est prêt ?",
            "enfant-f|Oui, papa.",
            "maman|Tu prends aussi tes bottes ?",
            "enfant-f|Oui, pour le château.",
            "narrateur|Victorina pose la main sur le tissu.",
            "narrateur|Le tissu est un peu rêche.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "chemin,fleuve,racine",
        [
            "papa|On met tes bottes.",
            "narrateur|Victorina enfile ses bottes.",
            "papa|Tu as fini tes bottes ?",
            "enfant-f|Oui, papa.",
            "maman|On ferme la porte.",
            "narrateur|Papa ferme la porte.",
            "maman|Tu as ton sac, Victorina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le chemin sent l'herbe, puis le fleuve.",
            "narrateur|Le seau tape un peu contre sa hanche.",
            "enfant-f|Mon château va être grand !",
            "maman|Oui, le sable t'attend.",
            "narrateur|Le sable luisant appelle, au bout du sentier.",
            "enfant-f|J'y vais avec le seau !",
            "narrateur|Elle pose le sac contre une racine.",
            "narrateur|Elle part avec le seau seul.",
            "narrateur|La poche vide manque sur sa hanche.",
            "enfant-f|Mon éclat !",
            "narrateur|Victorina s'arrête net.",
            "narrateur|Elle refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Le sac attend contre la racine.",
            "narrateur|Dans la poche, l'éclat de caillou pèse.",
            "papa|Tu le sens, dans le sac ?",
            "enfant-f|Oui.",
            "narrateur|Elle revient, prend le sac.",
            "narrateur|La sangle revient sur l'épaule.",
            "narrateur|Ils arrivent à la rive.",
            "narrateur|Le sable est frais sous les bottes.",
            "enfant-f|Je fais le mur.",
            "papa|Une poignée, puis une autre.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "sable,eau,mur",
        [
            "narrateur|Un mur rond apparaît, bas.",
            "maman|Il tient, ce mur.",
            "enfant-f|Une poignée, pour la tour.",
            "narrateur|Victorina appuie, sans se presser.",
            "narrateur|Elle ouvre la poche du sac.",
            "narrateur|L'éclat de caillou luit, pâle.",
            "enfant-f|Comme sur la table !",
            "narrateur|Elle le pose dans le mur frais.",
            "papa|Oui, tu l'as fait.",
            "enfant-f|Mon château est là.",
            "maman|Tu le vois, le petit éclat ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le seau rouge repose dans le sable.",
            "narrateur|L'eau du fleuve clapote contre la rive.",
            "narrateur|La table du jardin est loin.",
            "narrateur|Sur le mur, l'éclat de caillou garde un bord humide.",
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
        elif cid != "CHK_T0000_P0000":
            extra["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra)
    merged = dict(src)
    merged["fil_rouge"] = (
        "Sur la table du jardin, la poussière est tiède. Un éclat de caillou "
        "luit dans le dessin du château. Victorina veut le vrai château à la "
        "rive, maintenant. Elle pousse tout dans le sac : le zip mord, "
        "l'éclat roule sous le banc. Papa s'accroupit. Une chose, puis la "
        "suivante. Sur le sentier, elle pose le sac, part avec le seau. Elle "
        "refuse de foncer, reprend le sac. Dans le mur, l'éclat de caillou "
        "garde un bord humide."
    )
    merged["title"] = TITLE
    merged["characters"] = "Victorina, papa, maman"
    merged["setting"] = "jardin puis rive du fleuve"
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
        "Sur la table du jardin, la poussière est tiède. Victorina dessine un "
        "château du doigt. Un éclat de caillou luit : elle en fait la fenêtre "
        "du dessin. Elle veut le vrai château à la rive, **maintenant**. Elle "
        "pousse tout dans le sac d'un coup : le zip mord, le seau bascule, "
        "l'éclat roule sous le banc. Papa s'accroupit. Une chose, puis la "
        "suivante. Merci vécu, après la poche. Sur le sentier, elle pose le "
        "sac, part avec le seau. La poche vide manque. Elle refuse de foncer, "
        "reprend le sac. Dans le mur, l'éclat de caillou garde un bord "
        "humide, comme sur la table.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : table du jardin, poussière tiède, haie, fleuve, bottes, "
        "arrosoir.\n"
        "- Désir : porter le seau et l'éclat jusqu'à la rive, pour un château, "
        "maintenant.\n"
        "- Objet : sac, seau rouge, gourde, pelle, éclat de caillou.\n"
        "- Indice unique : éclat de caillou, vu dès l'ouverture, payé dans le "
        "mur.\n"
        "- Urgence douce : le sable de la rive l'appelle.\n"
        "- Imprévu 1 : tout d'un coup, zip qui mord, éclat sous le banc.\n"
        "- Cue : papa à la même hauteur, une chose puis la suivante. "
        "Un merci vécu, après l'éclat glissé.\n"
        "- Imprévu 2 (plus rusé) : elle pose le sac, part avec le seau seul.\n"
        "- Résolution : elle refuse de foncer, sent l'éclat dans la poche, "
        "reprend le sac.\n"
        "- Retour : mur qui tient, éclat-fenêtre, bord humide comme au jardin.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.001 (préparer le sac) greffée, jamais dite. La première "
        "idée (tout d'un coup) échoue. Le choix de Victorina change l'action. "
        "Un « en ce moment ». Un merci vécu. Adulte + question. Troupe D16 : "
        "Victorina, papa, maman.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : jardin puis rive du fleuve. ≠ bateau "
        "de Mila (port), ≠ pente de Nino.\n"
        "- Ouverture inventée (dessin dans la poussière), pas un gabarit v2.\n"
        "- Indice unique : éclat de caillou. Pas grain de miette/foin/feuille/"
        "paille/pin/pépin/pomme, pas éclat de pince/thermos/coquille/bouton/"
        "ticket/goutte/boucle/corde/caisse, pas trait de craie, merle, miel.\n"
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
