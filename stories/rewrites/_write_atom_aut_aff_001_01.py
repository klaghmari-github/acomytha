#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-01 — F-NAR-019. Le four du village. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-01"
N1 = 10
TITLE = "Le four du village"
FIL = (
    "Un souffle chaud passe entre les volets. Sur le rebord, un grain de "
    "miette brille. Amir veut le pain du four, maintenant, dans son sac. "
    "Il tire trop fort : la sangle reste coincée. Il refuse de foncer, "
    "prépare le sac, contourne une pierre. Au four, le grain de miette "
    "dore sur le pain qu'il porte."
)
CHARS = "Amir, papa"
SETTING = "cuisine au rebord, chemin poudreux, four du village"
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
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "grain de laine",
    "grain de grelot",
    "grain de parquet",
    "grain de lavande",
    "terre grise",
    "ancre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de miette",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous-texte=il_veut_le_pain_maintenant; "
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
            "intensite=1; destinataire=enfant; sous-texte=le_sac_tient_les_affaires; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="sac",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous-texte=il_prépare_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="pain",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; sous-texte=il_refuse_de_sauter_la_pierre; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de miette",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous-texte=le_grain_du_rebord_est_sur_le_pain; "
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
    "narrateur|La porte du four claque, au bout de la rue.",
    "narrateur|Un souffle chaud passe entre les volets.",
    "narrateur|Amir lève le nez, dans la cuisine.",
    "narrateur|Sur le rebord, un grain de miette brille.",
    "enfant-m|Il est tout petit, papa.",
    "papa|C'est un reste du pain d'hier.",
    "narrateur|Le grain dore comme un bout de soleil.",
    "narrateur|La nappe sent le bois et la farine.",
    "narrateur|Un carré de soleil touche le bois.",
    "papa|Amir, tu sens le pain ?",
    "enfant-m|Oui, papa.",
    "enfant-m|Je le veux chaud, maintenant.",
    "papa|Le four est tout près, au village.",
    "narrateur|Le sac bleu attend près de la porte.",
    "narrateur|En ce moment, Amir saisit le sac.",
    "enfant-m|Il est bleu, papa.",
    "papa|Oui, c'est le tien.",
    "papa|Prends de l'eau, pour le chemin.",
    "narrateur|Amir prend la gourde bleue.",
    "narrateur|Le bouchon est froid sous le doigt.",
    "narrateur|Il fait clic, tout petit.",
    "narrateur|Amir pose la gourde dans le sac.",
    "enfant-m|Elle est un peu froide.",
    "papa|Elle se réchauffera dehors.",
    "papa|Ton doudou voudra le four, lui aussi.",
    "enfant-m|Où est mon doudou ?",
    "narrateur|Le sac a un creux vide.",
    "narrateur|Le doudou n'est pas là.",
    "papa|Il attend sur le lit ?",
    "enfant-m|Je vais le chercher.",
    "narrateur|Amir part vers la chambre.",
    "narrateur|Le couloir sent le four, tiède.",
    "narrateur|Le plancher est un peu froid.",
    "narrateur|Sur le lit, le doudou attend.",
    "narrateur|Il sent l'oreiller, chaud.",
    "enfant-m|Te voilà.",
    "narrateur|Amir le serre contre sa joue.",
    "narrateur|Le tissu est chaud sous sa joue.",
    "papa|Tu l'as trouvé ?",
    "enfant-m|Oui.",
    "enfant-m|Il vient avec nous.",
    "narrateur|Amir revient vers la porte.",
    "enfant-m|Allez, on y va !",
    "narrateur|Il tire le sac, d'un coup.",
    "narrateur|La sangle glisse sous la chaise.",
    "narrateur|La chaise penche.",
    "narrateur|Le sac reste coincé.",
    "enfant-m|Ça ne veut pas, papa.",
    "narrateur|Amir ferme la bouche.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Ça serre, dans son ventre.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu regardes la sangle ?",
]

Q0001 = [
    "narrateur|Amir prépare le sac.",
    "narrateur|Où met-il les affaires ?",
]

C0001 = [
    "narrateur|Amir refuse de tirer plus fort.",
    "narrateur|Il pose un genou au sol.",
    "narrateur|La sangle est plate, sous le bois.",
    "enfant-m|Je la sors tout seul.",
    "narrateur|Il pousse la chaise, un peu.",
    "narrateur|La sangle se libère, lisse.",
    "enfant-m|Elle est libre.",
    "papa|Merci, Amir.",
    "narrateur|Il glisse le doudou dans le sac.",
    "narrateur|Le creux n'est plus vide.",
    "narrateur|Le livre attend sur le banc.",
    "enfant-m|Le livre aussi.",
    "narrateur|La couverture est lisse, un peu froide.",
    "narrateur|Amir veut tout mettre d'un coup.",
    "narrateur|Le livre tombe contre la sangle.",
    "enfant-m|Oh.",
    "narrateur|Il ne reprend pas trop vite.",
    "narrateur|Il écoute le sac, un instant.",
    "narrateur|Il pose le livre près de l'eau.",
    "enfant-m|Il est dedans.",
    "papa|Tu fermes, maintenant ?",
    "narrateur|Amir appuie sur la fermeture.",
    "narrateur|Ça fait un petit zzz.",
    "narrateur|Le sac bleu est fermé.",
    "papa|Le sac est prêt ?",
    "enfant-m|Oui, papa.",
    "narrateur|Amir pose la main sur le tissu.",
    "narrateur|Le tissu est un peu rêche.",
]

END = [
    "papa|On met tes chaussures ?",
    "narrateur|Amir enfile ses chaussures.",
    "narrateur|Une semelle est froide.",
    "papa|Tu as fini tes chaussures ?",
    "enfant-m|Oui, papa.",
    "papa|On ouvre la porte.",
    "narrateur|Papa ouvre la porte.",
    "narrateur|L'air sent le pain du village.",
    "narrateur|Le sac bleu tape contre sa hanche.",
    "enfant-m|On va voir le pain ?",
    "papa|Oui, il est tout près.",
    "narrateur|Ils marchent sur le chemin.",
    "narrateur|Le village sent le four, chaud.",
    "enfant-m|Je le vois, papa ?",
    "papa|Bientôt.",
    "papa|On continue.",
    "narrateur|Une poule traverse, plus loin.",
    "narrateur|Le chemin est un peu poudreux.",
    "narrateur|Une pierre ronde bloque le pas.",
    "enfant-m|Je saute par-dessus !",
    "narrateur|Amir recule d'un pas.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il contourne la pierre, lentement.",
    "narrateur|Le sac reste bien fermé.",
    "enfant-m|Ça sent bon.",
    "papa|Oui, très bon.",
    "narrateur|Amir sent le pain sur sa langue.",
]

FIN = [
    "narrateur|Ils s'arrêtent devant le four tiède.",
    "narrateur|La chaleur touche les joues d'Amir.",
    "enfant-m|Le pain est là.",
    "papa|Oui, tout chaud.",
    "narrateur|Un pain rond attend sur la planche.",
    "narrateur|Sur la croûte, un grain de miette brille.",
    "enfant-m|Comme sur le rebord, papa !",
    "papa|Tu le portes, toi ?",
    "enfant-m|Oui, dans mon sac.",
    "narrateur|Amir ouvre le sac, sans se presser.",
    "narrateur|Il glisse le pain contre le doudou.",
    "narrateur|Le sac repose contre sa hanche.",
    "enfant-m|On le sent, papa.",
    "papa|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est chaud.",
    "narrateur|Le four tiède touche ses joues.",
    "narrateur|Le grain de miette dore sur le pain.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "volets,sac",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "le sac",
                    "accepted_examples": "le sac | dans le sac | il met | elle met | mettre",
                    "retry_prompt": "Il met les affaires dans le sac. Où les met Amir ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "sac,fermeture",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "chemin,pas",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "four,pain",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "grain de miette" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "grain de miette" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
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
        "- **Leçon :** AUT.AFF.001 — préparer le sac, porter, oser (vécue)\n"
        "- **Personnages :** Amir, papa\n"
        "- **Lieu :** cuisine au rebord, chemin poudreux, four du village\n"
        "- **Indice unique :** grain de miette (rebord → croûte du pain)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La porte du four claque au bout de la rue. Un souffle chaud passe "
        "entre les volets. Sur le rebord, un grain de miette brille. Amir veut "
        "le pain chaud **maintenant**, dans son sac. Il met la gourde, cherche "
        "le doudou, puis tire trop fort : la sangle reste coincée. Première "
        "idée ratée. Il refuse de foncer, libère la sangle, range le doudou et "
        "le livre (le livre tombe : il ne reprend pas trop vite). Sur le chemin, "
        "une pierre : il recule, contourne. Au four, le grain de miette dore "
        "sur le pain. Il le glisse dans son sac. Les joues sont chaudes.\n\n"
        "## Vécu\n\n"
        "Amir veut le pain **maintenant**. Impatience, puis épaules qui tombent "
        "quand le sac résiste. Papa se baisse, pose une question, ne récite "
        "pas la règle. Amir agit : genou au sol, sangle, sac, pain porté. "
        "Merci vécu après la sangle. Fin : le grain du début est sur la croûte.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (claque du four, souffle, grain), pas « déjà le pain ».\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Leçon non dite : il prépare, porte, ose. Pas de morale.\n"
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
