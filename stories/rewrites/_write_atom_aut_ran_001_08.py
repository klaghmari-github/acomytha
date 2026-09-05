#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-08 — F-NAR-019. Le pont de Nino. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-08"
N2 = 15
TITLE = "Le pont de Nino"
INDICE = "éclat de citron"
FIL = (
    "L'odeur de citron arrive avant le sol sec. Sur un carreau mouillé, "
    "un éclat de citron brille. Nino veut le pont du tapis, maintenant, "
    "pour la voiture jusqu'au canapé, puis le t-shirt chaud. Un cube "
    "glisse : l'arche s'écroule sur la voiture. Il cherche dans le linge, "
    "sous le canapé, puis prend toute la pile : les cubes s'éparpillent. "
    "Il refuse de foncer, pose un cube, retrouve la voiture. Sur le "
    "carreau libre, l'éclat de citron tient."
)
CHARS = "Nino, papa, maman"
SETTING = "salon après la serpillière au citron, pile de linge chaud, après-midi"
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
    "on va ranger",
    "tu ranges",
    "grain de miette",
    "grain de sable",
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
    "éclat de orange",
    "éclat d'orange",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat de ecorce",
    "éclat de laine",
    "éclat de lampe",
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
        emphasis="éclat de citron",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_pont_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="voiture",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_voiture_est_sous_les_cubes; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="caisse",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_pose_un_cube_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="t-shirt",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_tirer_toute_la_pile; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de citron",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_carreau; "
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
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
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
    "narrateur|L'odeur de citron arrive avant le sol sec.",
    "narrateur|Papa tord la serpillière au-dessus du seau.",
    "narrateur|Le seau fait un petit plouf.",
    "maman|Ça sent le propre.",
    "papa|Oui, le citron a fini.",
    "narrateur|Sur un carreau mouillé, un éclat de citron brille.",
    "enfant-m|Il est jaune, papa.",
    "papa|C'est le citron, sur le carreau.",
    "narrateur|Les carreaux sont un peu frais.",
    "narrateur|Puis le tapis du salon est épais.",
    "maman|Le sol est propre, Nino.",
    "papa|Tu restes sur le tapis ?",
    "enfant-m|Oui, le sol est mouillé.",
    "narrateur|Près du canapé, une pile de linge attend.",
    "narrateur|Un petit t-shirt reste chaud, au sommet.",
    "enfant-m|Je veux mon pont, maintenant !",
    "maman|Pendant que le sol sèche ?",
    "enfant-m|Oui, un pont jusqu'au canapé.",
    "narrateur|En ce moment, Nino saisit un cube.",
    "narrateur|Le cube bleu pèse un peu, dans sa main.",
    "narrateur|Il pose le cube sur le tapis épais.",
    "narrateur|Le bois tape, un petit clic.",
    "enfant-m|C'est le pont du tapis.",
    "papa|Un pont bien solide ?",
    "enfant-m|Oui, il est solide.",
    "maman|Il va jusqu'où, ton pont ?",
    "enfant-m|Jusqu'au canapé, maman.",
    "narrateur|Nino pose un cube à gauche.",
    "narrateur|Puis un cube à droite.",
    "narrateur|Le pont a une arche.",
    "maman|Je vois l'arche, Nino.",
    "enfant-m|Une petite voiture peut passer.",
    "papa|On essaie ?",
    "narrateur|La petite voiture rouge attend près du tapis.",
    "enfant-m|Toi, tu vas sous le pont.",
    "narrateur|Nino la pousse vers l'arche.",
    "narrateur|Un cube glisse.",
    "narrateur|L'arche a un trou.",
    "enfant-m|Oh, elle ne passe pas.",
    "papa|Le cube est tombé.",
    "narrateur|Nino repose le cube, trop vite.",
    "narrateur|Le cube penche, de travers.",
    "narrateur|La voiture bute, une seconde fois.",
    "enfant-m|Ça ne veut pas !",
    "narrateur|Le sourire de Nino disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "maman|Tu regardes le cube, d'abord ?",
    "enfant-m|Oui, maman.",
    "narrateur|Il pose le cube, sans se presser.",
    "narrateur|L'arche redevient ronde.",
    "narrateur|La voiture passe dessous.",
    "enfant-m|Elle est passée !",
    "maman|Elle rentre à la maison ?",
    "enfant-m|Oui, puis on s'assoit.",
    "narrateur|Nino veut le t-shirt chaud.",
    "enfant-m|Maintenant, le t-shirt !",
    "narrateur|Il pousse la voiture trop fort.",
    "narrateur|Trois cubes tombent d'un coup.",
    "narrateur|L'arche s'écroule sur la voiture.",
    "enfant-m|Oh.",
    "papa|Le pont est tombé.",
    "enfant-m|Où est ma petite voiture ?",
    "maman|Dans la pile de linge ?",
    "narrateur|Nino fouille le t-shirt chaud.",
    "narrateur|Le tissu sent le savon.",
    "narrateur|Pas de voiture.",
    "enfant-m|Sous le canapé ?",
    "narrateur|Il se penche.",
    "narrateur|De la poussière, un fil.",
    "enfant-m|Elle est perdue.",
    "narrateur|L'éclat de citron tremble, sur le carreau.",
    "enfant-m|Je prends tout, d'un coup !",
    "narrateur|Il saisit la pile trop vite.",
    "narrateur|Les cubes glissent entre ses doigts.",
    "narrateur|Le tapis disparaît sous les cubes.",
    "enfant-m|Ça ne veut pas, papa.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu regardes sous les cubes ?",
]

Q0001 = [
    "narrateur|Nino cherche sa petite voiture.",
    "narrateur|Où est-elle ?",
]

C0001 = [
    "narrateur|Nino laisse la pile de cubes.",
    "narrateur|Un genou se pose sur le tapis.",
    "narrateur|Sa main trouve un cube bleu.",
    "enfant-m|Je le mets, tout seul.",
    "narrateur|Le cube glisse dans la caisse.",
    "narrateur|Toc.",
    "narrateur|Le bois sent un peu le citron.",
    "maman|Tu regardes bien dessous ?",
    "enfant-m|Oui, maman.",
    "narrateur|Un bout de tapis reparaît.",
    "narrateur|Le cube jaune suit le bleu.",
    "narrateur|Toc.",
    "enfant-m|Je sors le reste, d'un coup !",
    "narrateur|Nino tire trop fort, en bas.",
    "narrateur|Deux cubes retombent, comme un toit.",
    "enfant-m|Oh.",
    "narrateur|Cette fois, il ne reprend pas.",
    "narrateur|Il écoute le salon, un instant.",
    "narrateur|Près des cubes, l'éclat de citron brille.",
    "enfant-m|Il est là.",
    "narrateur|Nino refuse de foncer.",
    "narrateur|Il écarte un cube, lentement.",
    "narrateur|Un toit minuscule brille.",
    "enfant-m|Ma voiture !",
    "narrateur|La petite voiture était sous l'arche.",
    "narrateur|Elle sent le bois des cubes.",
    "narrateur|Nino la tient dans la paume.",
    "narrateur|Les roues sont un peu froides.",
    "papa|Merci, Nino.",
    "enfant-m|Elle était dessous.",
    "narrateur|La caisse a presque tous les cubes.",
    "narrateur|Le tapis est libre, au milieu.",
    "maman|Le t-shirt peut venir ?",
    "enfant-m|Oui, maman.",
]

END = [
    "papa|On prend le t-shirt ?",
    "narrateur|Nino va vers la pile tiède.",
    "enfant-m|Je prends tout !",
    "narrateur|Il tire trop fort sur le tas.",
    "narrateur|Une chaussette tombe, molle.",
    "enfant-m|Oh.",
    "narrateur|Nino s'arrête net.",
    "narrateur|Il refuse de foncer.",
    "enfant-m|Attends, je regarde.",
    "narrateur|Il prend le t-shirt, seul.",
    "maman|Il est chaud, celui-là.",
    "enfant-m|Oui, maman.",
    "narrateur|Maman lui tend le tissu.",
    "narrateur|Nino l'enfile.",
    "narrateur|Le tissu sent le savon, bien chaud.",
    "papa|La caisse, Nino ?",
    "enfant-m|Je la pousse.",
    "narrateur|Nino pousse la caisse près du canapé.",
    "narrateur|Le bois glisse un peu.",
    "papa|On s'assoit ?",
    "enfant-m|Oui, papa.",
    "narrateur|Nino grimpe sur le canapé.",
    "narrateur|La petite voiture est sur ses genoux.",
    "maman|Tu veux un verre d'eau ?",
    "enfant-m|Oui, maman.",
    "narrateur|L'eau est fraîche, après le citron.",
    "narrateur|Nino boit une gorgée.",
    "papa|Le pont a fini sa journée.",
    "enfant-m|La voiture aussi.",
]

FIN = [
    "narrateur|Ils s'assoient près de la pile tiède.",
    "narrateur|La chaleur touche les joues de Nino.",
    "enfant-m|La voiture est sur mes genoux.",
    "maman|Toi aussi, tu es au chaud.",
    "enfant-m|Comme sur le carreau, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, le petit jaune.",
    "narrateur|Nino glisse la voiture sans se presser.",
    "narrateur|Le métal repose contre sa hanche.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est chaud.",
    "papa|Le carreau est libre, Nino.",
    "enfant-m|Comme au début, papa.",
    "narrateur|Le citron reste dans l'air.",
    "narrateur|L'éclat de citron tient sur le carreau.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    expected = {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in expected]
    extra = expected - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "serpillière,cubes,voiture",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "la petite voiture",
                    "accepted_examples": (
                        "la petite voiture | la voiture | sous le pont "
                        "| sous l'arche | sous les cubes | dessous"
                    ),
                    "retry_prompt": "Il cherche sous les cubes. Où est la petite voiture ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "caisse,bois",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "linge,canapé",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "citron,canapé",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    for m in re.finditer(r"éclat d['e]\s*\w+", blob):
        got = m.group(0)
        if got not in ("éclat de citron",):
            raise SystemExit(f"{SID}: indice non unique: {got}")
    if not all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in chunks
    ):
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
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")

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
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** AUT.RAN.001 — ranger (vécue : voiture sous l'arche)\n"
        "- **Personnages :** Nino, papa, maman\n"
        "- **Lieu :** salon après la serpillière au citron, pile de linge "
        "chaud, après-midi\n"
        "- **Indice unique :** éclat de citron (carreau mouillé → carreau "
        "libre)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "L'odeur de citron arrive avant le sol sec. Papa tord la "
        "serpillière. Sur un carreau mouillé, un éclat de citron brille. "
        "Nino veut le pont du tapis **maintenant**, pour la voiture jusqu'au "
        "canapé, puis le t-shirt chaud. Il pose trop vite : un cube glisse, "
        "l'arche s'écroule sur la voiture. Première idée : dans le linge, "
        "sous le canapé. Rien. Il prend toute la pile d'un coup : les cubes "
        "s'éparpillent. Sourire parti, épaules basses. Papa se baisse. Nino "
        "refuse de foncer, pose un cube, tire trop fort : deux cubes "
        "retombent. Il écoute, voit l'éclat, écarte un cube. La voiture "
        "était dessous. Merci vécu. Il tire le tas de linge : une "
        "chaussette tombe. Il s'arrête, prend le t-shirt seul. Sur le "
        "carreau libre, l'éclat de citron tient. Les joues sont chaudes.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : serpillière au citron, carreaux frais, tapis épais, pile "
        "de linge, t-shirt chaud.\n"
        "- Désir : le pont du tapis, maintenant, puis s'asseoir au chaud.\n"
        "- Objet : cubes, petite voiture rouge, t-shirt, caisse.\n"
        "- Indice unique : éclat de citron, vu dès l'ouverture, payé sur le "
        "carreau libre.\n"
        "- Imprévu 1 : cube trop vite, arche écroulée, voiture perdue.\n"
        "- Première idée : linge, canapé, toute la pile. Échec.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la voiture.\n"
        "- Imprévu 2 (plus rusé) : il tire le tas de linge, une chaussette "
        "tombe.\n"
        "- Résolution : il refuse de foncer, un cube, puis le t-shirt seul.\n"
        "- Retour : canapé, eau fraîche, éclat du début sur le carreau.\n\n"
        "## Vécu\n\n"
        "Nino veut le pont **maintenant**. Impatience, puis épaules qui "
        "tombent quand la pile résiste. Papa se baisse, pose une question, "
        "ne récite pas la règle. Nino agit : genou au tapis, cube dans la "
        "caisse, voiture retrouvée. Merci vécu après la voiture. Fin : "
        "l'éclat du début tient sur le carreau.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (odeur de citron avant le sol sec, serpillière, "
        "éclat), pas « joue au salon ».\n"
        "- Monde du dump (salon, citron, pile de linge, pont, voiture), "
        "distinct de RAN.001-01 (nappe, vanille, tour) et RAN.001-04 "
        "(cabane sous table).\n"
        "- Tic dump « encore le citron » jeté. Tics « encore / déjà / tout "
        "doux / tout calme » retirés.\n"
        "- Leçon non dite : la voiture reparaît quand les cubes vont dans "
        "la caisse. Pas de morale, pas « on va ranger ».\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique : éclat de citron. Pas grain de miette/foin/"
        "feuille/paille/pin/pépin/pomme/sable, pas éclat de pince/thermos/"
        "coquille/bouton/ticket/goutte/boucle/corde/caisse/marche/caillou/"
        "liste/clé/cuillère/sonnette/horloge/tasse/orange/colle/lessive/"
        "vitre/casserole/carreau/grain/nappe/boîte/farine/ombre/écorce/"
        "laine/lampe, pas pli de voile, point de gouttière, trait de "
        "craie/vitre, merle, miel.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        f"- N2 ≤ 15. {nwords} mots. `check()` OK. Pas apply.\n\n"
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
