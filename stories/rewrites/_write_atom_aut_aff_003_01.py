#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-01 — F-NAR-019. Le seau jaune de Raphaël. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-01"
N1 = 10
TITLE = "Le seau jaune de Raphaël"
FIL = (
    "La barrière du parc cliquette. Sur le rebord jaune, un grain de sable "
    "brille. Raphaël veut le seau plein, maintenant, à la maison. Il verse "
    "trop vite, puis court avec le seau seul : l'anse glisse. Il refuse de "
    "foncer, met le manteau, reprend le doudou. Devant la porte, le grain "
    "de sable dore sur le rebord."
)
CHARS = "Raphaël, papa"
SETTING = "parc, bac à sable, banc, chemin vers la maison"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent", "tout bas")
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
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de carotte",
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
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de sable",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_seau_plein_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="affaires",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_reprend_manteau_doudou_seau; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="manteau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_s_habille_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="racine",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_sauter_la_racine; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de sable",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_grain_du_bac_est_sur_le_rebord; "
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
    "narrateur|La barrière du parc cliquette, sous le vent.",
    "narrateur|Un carré d'ombre coupe le bac.",
    "narrateur|Le sable est frais, au fond.",
    "narrateur|Sur le rebord jaune, un grain de sable brille.",
    "enfant-m|Il est tout petit, papa.",
    "papa|C'est un grain du bac.",
    "narrateur|Le seau jaune attend près des pieds.",
    "narrateur|Le bois du banc sent le soleil.",
    "narrateur|Un doudou gris est assis dessus.",
    "narrateur|Le manteau bleu dort à côté.",
    "narrateur|L'air sent l'herbe et le sable chaud.",
    "papa|Raphaël, tu sens le sable ?",
    "enfant-m|Oui, papa.",
    "enfant-m|Je le verse, maintenant !",
    "papa|Le bac est frais, hein ?",
    "enfant-m|Oui.",
    "enfant-m|Il est frais.",
    "narrateur|En ce moment, Raphaël saisit le seau.",
    "narrateur|Le plastique est lisse, un peu chaud.",
    "narrateur|Une poignée glisse, puis une autre.",
    "narrateur|Ça fait chh, contre le plastique.",
    "enfant-m|Ça chante, papa.",
    "papa|Oui, le sable chante.",
    "narrateur|Raphaël veut le seau plein.",
    "enfant-m|Je le ramène à la maison.",
    "narrateur|Le seau se remplit, lourd.",
    "enfant-m|Il est jaune, papa.",
    "papa|Oui, bien jaune.",
    "papa|C'est l'heure, Raphaël.",
    "papa|On rentre.",
    "enfant-m|Attends, je le remplis !",
    "narrateur|Il verse trop vite, d'un coup.",
    "narrateur|Le seau penche sur le bord.",
    "narrateur|Une vague de sable touche ses chaussures.",
    "enfant-m|Oh.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|Je prends le seau, et je cours !",
    "narrateur|Il marche vers la barrière.",
    "narrateur|Le seau tapote contre sa jambe.",
    "papa|Attends, Raphaël.",
    "papa|Ton manteau est au banc.",
    "narrateur|Raphaël s'arrête.",
    "narrateur|Il regarde derrière lui.",
    "narrateur|Le banc n'est pas vide.",
    "enfant-m|Je reviens après !",
    "narrateur|Il tire l'anse, d'un coup.",
    "narrateur|L'anse glisse entre ses doigts.",
    "narrateur|Le seau tape le bord du bac.",
    "narrateur|Le grain de sable bascule, puis tient.",
    "enfant-m|Ça ne veut pas, papa.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu regardes le banc ?",
]

Q0001 = [
    "narrateur|Raphaël reprend ses affaires.",
    "narrateur|Que fait-il, avant de partir ?",
]

C0001 = [
    "narrateur|Raphaël refuse de tirer plus fort.",
    "narrateur|Il pose un genou au sable.",
    "narrateur|L'anse est libre, un instant.",
    "enfant-m|Je le sors tout seul.",
    "narrateur|Il pose le seau près du banc.",
    "enfant-m|Le manteau, et le doudou.",
    "narrateur|Il prend les deux, d'un coup.",
    "narrateur|Le manteau glisse, tombe.",
    "narrateur|Le doudou roule sous le banc.",
    "enfant-m|Oh.",
    "narrateur|Il ne reprend pas trop vite.",
    "narrateur|Il écoute le parc, un instant.",
    "narrateur|Sur le rebord, le grain de sable brille.",
    "enfant-m|Il est là.",
    "papa|Tu mets le manteau ?",
    "narrateur|Raphaël prend le manteau bleu.",
    "narrateur|Une manche entre, facile.",
    "narrateur|L'autre manche reste coincée, derrière.",
    "enfant-m|Je tire !",
    "narrateur|Il s'arrête.",
    "narrateur|Raphaël refuse de foncer.",
    "narrateur|Il recule le bras, lentement.",
    "narrateur|La manche se libère, lisse.",
    "papa|Merci, Raphaël.",
    "narrateur|Il se baisse près du bois.",
    "narrateur|Ses doigts trouvent le doudou gris.",
    "enfant-m|Te voilà.",
    "narrateur|Il le serre contre sa joue.",
    "papa|Tu as le seau aussi ?",
    "enfant-m|Oui.",
    "enfant-m|Le seau jaune.",
    "narrateur|Ses affaires sont avec lui.",
    "papa|On peut partir ?",
    "enfant-m|Oui, papa.",
    "narrateur|Raphaël pose la main sur l'anse.",
    "narrateur|L'anse est un peu rêche.",
]

END = [
    "papa|On prend le chemin ?",
    "narrateur|Raphaël serre le manteau contre lui.",
    "narrateur|Une manche est tiède.",
    "papa|Tu as ton manteau ?",
    "enfant-m|Oui, papa.",
    "papa|On ouvre la barrière.",
    "narrateur|Papa ouvre la barrière.",
    "narrateur|L'air sent l'herbe coupée.",
    "narrateur|Le seau jaune tape contre sa hanche.",
    "enfant-m|On rentre avec le seau ?",
    "papa|Oui, il est à toi.",
    "narrateur|Ils marchent sur le chemin.",
    "narrateur|Le doudou est contre lui.",
    "enfant-m|Je la vois, papa ?",
    "papa|Bientôt.",
    "papa|On continue.",
    "narrateur|Une branche traverse, plus loin.",
    "narrateur|Le chemin est un peu poudreux.",
    "narrateur|Une racine ronde bloque le pas.",
    "enfant-m|Je saute par-dessus !",
    "narrateur|Raphaël recule d'un pas.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il contourne la racine, lentement.",
    "narrateur|Le seau reste bien droit.",
    "enfant-m|Ça sent bon.",
    "papa|Oui, très bon.",
    "narrateur|Raphaël sent le sable sur sa langue.",
]

FIN = [
    "narrateur|Ils s'arrêtent devant la porte tiède.",
    "narrateur|La chaleur touche les joues de Raphaël.",
    "enfant-m|La maison est là.",
    "papa|Oui, tout près.",
    "narrateur|Le seau jaune attend dans ses mains.",
    "narrateur|Sur le rebord, un grain de sable brille.",
    "enfant-m|Comme sur le bac, papa !",
    "papa|Tu le portes, toi ?",
    "enfant-m|Oui, avec le doudou.",
    "narrateur|Raphaël ouvre la porte, sans se presser.",
    "narrateur|Il glisse le seau près du tapis.",
    "narrateur|Le manteau repose sur le crochet.",
    "enfant-m|On le sent, papa.",
    "papa|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est chaud.",
    "narrateur|La porte tiède touche ses joues.",
    "narrateur|Le grain de sable dore sur le rebord.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "barrière,sable",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "reprendre",
                    "accepted_examples": (
                        "reprendre | ses affaires | il reprend | avant de partir "
                        "| manteau | doudou | seau"
                    ),
                    "retry_prompt": "Il reprend ses affaires. Que fait Raphaël ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "banc,manteau",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "chemin,pas",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "porte,seau",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "grain de sable" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "grain de sable" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if not all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks):
        raise SystemExit(f"{SID}: TTS incomplet")

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
        "- **Leçon :** AUT.AFF.003 — s'habiller, reprendre ses affaires, oser (vécue)\n"
        "- **Personnages :** Raphaël, papa\n"
        "- **Lieu :** parc, bac à sable, banc, chemin vers la maison\n"
        "- **Indice unique :** grain de sable (rebord du seau → rebord à la porte)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La barrière du parc cliquette sous le vent. Un carré d'ombre coupe "
        "le bac. Sur le rebord jaune, un grain de sable brille. Raphaël veut "
        "le seau plein **maintenant**, à la maison. Il verse trop vite : le "
        "sable tombe. Première idée : courir avec le seau seul. L'anse glisse. "
        "Il refuse de foncer, pose le seau, prend manteau et doudou d'un coup : "
        "ça tombe. Il met le manteau tout seul (manche coincée : il recule le "
        "bras). Merci vécu. Sur le chemin, une racine : il recule, contourne. "
        "À la porte, le grain de sable dore sur le rebord. Le seau est près "
        "du tapis. Les joues sont chaudes.\n\n"
        "## Vécu\n\n"
        "Raphaël veut le seau **maintenant**. Impatience, puis épaules qui "
        "tombent quand l'anse résiste. Papa se baisse, pose une question, ne "
        "récite pas la règle. Raphaël agit : genou au sable, manteau, doudou, "
        "seau porté. Merci vécu après la manche. Fin : le grain du début est "
        "sur le rebord, à la maison.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (barrière, ombre, grain), pas « joue au parc ».\n"
        "- Monde du dump (parc, bac à sable), distinct de AFF.001 / AFF.002.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Leçon non dite : il s'habille, reprend, ose. Pas de morale.\n"
        "- Merci vécu. Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action plus vive.\n"
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
