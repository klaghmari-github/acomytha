#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-07 — F-NAR-019. La vache d'or. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-07"
N3 = 16
TITLE = "La vache d'or"
FIL = (
    "La fenêtre laisse entrer la terre mouillée. Un papillon frappe la vitre. "
    "Sur le flanc de la vache, un éclat de lampe brille. Aniss veut le collier "
    "et l'histoire au lit, maintenant. Le cheval bascule : le mouton recouvre "
    "la vache. Il cherche sous le lit, dans le cercle : rien. Il prend tout "
    "d'un coup : les bêtes s'éparpillent. Il refuse de foncer, pose le cheval, "
    "retrouve la vache. Sur l'oreiller, l'éclat de lampe tient au flanc."
)
CHARS = "Aniss, papa, maman"
SETTING = "chambre, soir, lampe ronde, papillon de nuit, fenêtre entrouverte"
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
        emphasis="éclat de lampe",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_vache_et_l_histoire_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="vache",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_vache_est_sous_le_mouton; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de lampe",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_pose_une_bete_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="couverture",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_tirer_la_couverture; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de lampe",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_flanc; "
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
    "narrateur|La fenêtre laisse entrer un air de terre mouillée, un peu froid.",
    "narrateur|Un papillon de nuit se pose, puis frappe la vitre du bout des ailes.",
    "narrateur|Sa silhouette tremble un peu, sur le tapis.",
    "maman|Tu entends les ailes, Aniss ?",
    "enfant-m|Oui, maman.",
    "narrateur|Le plancher craque sous le pas de papa.",
    "papa|La lampe ronde est allumée.",
    "narrateur|Elle chauffe le bois des bêtes, une à une.",
    "narrateur|Sur le flanc de la vache, un éclat de lampe brille.",
    "enfant-m|Il est tout petit, papa.",
    "papa|C'est un éclat de lampe.",
    "narrateur|La vache est lisse, un peu chaude sous le doigt.",
    "narrateur|Le cheval sent le bois, sec et clair.",
    "enfant-m|C'est une ferme, maman.",
    "maman|Une ferme sur le tapis.",
    "narrateur|En ce moment, Aniss pose la vache au milieu du tapis.",
    "narrateur|Il pose le cheval à côté, tap.",
    "narrateur|Le mouton vient après, laine peinte, un peu rêche.",
    "papa|Elles sont bien, tes bêtes.",
    "enfant-m|La vache mange, papa.",
    "maman|Et le mouton ?",
    "enfant-m|Il dort près de la vache.",
    "narrateur|Aniss sort des perles d'une coupelle.",
    "narrateur|Elles sont rondes, un peu froides dans la paume.",
    "enfant-m|Je fais un collier, maintenant !",
    "maman|Pour la vache d'or ?",
    "enfant-m|Oui, et après l'histoire au lit.",
    "narrateur|Aniss enfile une perle, clic.",
    "narrateur|Puis une autre, clic, contre la première.",
    "narrateur|Les perles font un tout petit bruit.",
    "narrateur|Il pose le collier sur le cou de la vache.",
    "enfant-m|Elle est belle.",
    "papa|Oui, elle est belle.",
    "enfant-m|L'histoire, maintenant, maman !",
    "maman|Près de toi, au lit ?",
    "enfant-m|La vache vient aussi.",
    "narrateur|Maman s'approche du tapis, trop près des bêtes.",
    "narrateur|Le cheval bascule.",
    "narrateur|Une perle roule sous le lit.",
    "narrateur|Le mouton glisse sur la vache, et la cache.",
    "enfant-m|Oh.",
    "papa|La ferme a bougé.",
    "enfant-m|Où est ma vache ?",
    "maman|Sous le lit, peut-être ?",
    "narrateur|Aniss se penche dans l'ombre, près du bois.",
    "narrateur|Le bois du lit est froid, un peu rugueux.",
    "narrateur|Pas de vache.",
    "enfant-m|Dans le cercle de la lampe ?",
    "narrateur|Il cherche au milieu de la lumière ronde.",
    "narrateur|Des perles, le cheval, le mouton.",
    "enfant-m|Elle est perdue.",
    "enfant-m|Je prends tout, d'un coup !",
    "narrateur|Il saisit le cheval et le mouton trop vite.",
    "narrateur|Les perles glissent entre ses doigts.",
    "narrateur|Le tapis disparaît sous les bêtes.",
    "enfant-m|Ça ne veut pas, papa.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Le sourire d'Aniss disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tu regardes sous les bêtes ?",
]

Q0001 = [
    "narrateur|Aniss cherche sa vache.",
    "narrateur|Où est-elle ?",
]

C0001 = [
    "narrateur|Aniss refuse de prendre toute la pile d'un coup.",
    "narrateur|Il pose un genou au tapis, près des perles.",
    "narrateur|Le cheval reste près de sa main.",
    "enfant-m|Je le mets tout seul.",
    "narrateur|Il glisse le cheval dans la caisse.",
    "narrateur|Toc.",
    "narrateur|Le bois sent un peu la forêt.",
    "maman|Tu regardes bien dessous ?",
    "enfant-m|Oui, maman.",
    "narrateur|Un bout de tapis reparaît, gris et doux.",
    "narrateur|Une perle va dans la caisse.",
    "narrateur|Clic.",
    "enfant-m|Je sors le reste, d'un coup !",
    "narrateur|Il tire trop fort sur le mouton.",
    "narrateur|Deux perles retombent, comme un petit toit.",
    "enfant-m|Oh.",
    "narrateur|Il ne reprend pas trop vite.",
    "narrateur|Il écoute la chambre, un instant.",
    "narrateur|Sur le dos du mouton, l'éclat de lampe brille.",
    "enfant-m|Il est là.",
    "narrateur|Aniss refuse de foncer.",
    "narrateur|Il soulève le mouton, lentement.",
    "narrateur|Un dos lisse, un peu chaud, apparaît.",
    "enfant-m|Ma vache !",
    "narrateur|La vache était sous le mouton.",
    "narrateur|Le collier tient autour du cou.",
    "narrateur|Aniss la serre contre sa joue.",
    "papa|Merci, Aniss.",
    "enfant-m|Elle dormait dessous.",
    "narrateur|La caisse a presque toutes les bêtes.",
    "narrateur|Le tapis est libre, au milieu.",
    "maman|On peut aller au lit ?",
    "enfant-m|Oui, avec la vache.",
]

END = [
    "papa|Tu grimpes avec elle ?",
    "narrateur|Aniss grimpe sur le lit, la vache dans la main.",
    "narrateur|La vache est sur la couverture.",
    "narrateur|Le collier brille un peu, près du genou.",
    "maman|Je m'assoie ?",
    "enfant-m|Oui, maman.",
    "narrateur|Maman s'assoit au bord, près de l'oreiller.",
    "narrateur|Sa voix est basse, près de lui.",
    "papa|Tu veux un peu d'eau ?",
    "enfant-m|Une gorgée, papa.",
    "narrateur|L'eau est tiède.",
    "narrateur|Aniss pose la vache contre l'oreiller.",
    "enfant-m|Je tire la couverture !",
    "narrateur|Aniss s'arrête.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il recule le pli, lentement.",
    "narrateur|La couverture se pose, plate.",
    "papa|L'histoire peut s'asseoir.",
    "narrateur|Le papillon de nuit repose sur la vitre.",
    "maman|On écoute, maintenant.",
    "enfant-m|La vache écoute aussi.",
    "papa|Oui, on écoute avec elle.",
    "narrateur|La lampe tient son cercle chaud.",
    "narrateur|L'air sent la terre mouillée.",
]

FIN = [
    "narrateur|Ils s'assoient près de la couverture tiède.",
    "narrateur|La chaleur touche les joues d'Aniss.",
    "enfant-m|La vache est là.",
    "maman|Oui, près de toi.",
    "narrateur|Le collier tient un tout petit reflet.",
    "enfant-m|Comme l'éclat de lampe, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, sur le flanc.",
    "narrateur|Aniss glisse la vache sans se presser.",
    "narrateur|Le bois repose contre sa hanche.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est chaud.",
    "narrateur|Le papillon repose ses ailes.",
    "narrateur|L'éclat de lampe tient sur le flanc.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "papillon,perles",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "la vache",
                    "accepted_examples": (
                        "la vache | vache | sous le mouton | sous la ferme "
                        "| dessous | sous les bêtes"
                    ),
                    "retry_prompt": "Il cherche sous les bêtes. Où est la vache ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "caisse,bois",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "couverture,eau",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "lampe,vache",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de lampe" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de lampe" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
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
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** AUT.RAN.001 — ranger (vécue : vache sous le mouton)\n"
        "- **Personnages :** Aniss, papa, maman\n"
        "- **Lieu :** chambre, soir, lampe ronde, papillon de nuit, "
        "fenêtre entrouverte\n"
        "- **Indice unique :** éclat de lampe (flanc de la vache → flanc "
        "sur l'oreiller)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La fenêtre laisse entrer un air de terre mouillée. Un papillon de "
        "nuit frappe la vitre. Sur le flanc de la vache, un éclat de lampe "
        "brille. Aniss veut le collier et l'histoire au lit **maintenant**. "
        "Maman s'approche : le cheval bascule, une perle roule, le mouton "
        "cache la vache. Première idée : sous le lit, dans le cercle. Rien. "
        "Il prend tout d'un coup : les bêtes s'éparpillent. Sourire parti, "
        "épaules basses. Papa s'accroupit. Aniss refuse de foncer, pose le "
        "cheval, tire trop fort : deux perles retombent. Il écoute, voit "
        "l'éclat, soulève le mouton. La vache était dessous. Merci vécu. "
        "Il tire la couverture : il s'arrête, recule le pli. Sur l'oreiller, "
        "l'éclat tient au flanc. Les joues sont chaudes.\n\n"
        "## Vécu\n\n"
        "Aniss veut le collier et l'histoire **maintenant**. Impatience, "
        "puis épaules qui tombent quand la pile résiste. Papa s'accroupit, "
        "pose une question, ne récite pas la règle. Aniss agit : genou au "
        "tapis, cheval dans la caisse, vache retrouvée. Merci vécu après "
        "la vache. Fin : l'éclat du début tient sur le flanc.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (air de terre, papillon, éclat sur le flanc), "
        "pas « joue au salon », pas « Tout doucement ».\n"
        "- Monde du dump (chambre, soir, lampe ronde, papillon, fenêtre "
        "entrouverte), distinct de RAN.001-01..006 (nappe, cacao, pain, "
        "cabane, voiture rouge, chaussettes).\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout doucement » "
        "retirés. Pas de merle, pas de miel.\n"
        "- Leçon non dite : la vache reparaît quand les bêtes vont dans "
        "la caisse. Pas de morale, pas « on va ranger ».\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de lampe » nommé à l'ouverture, revu sur "
        "le mouton, payé sur l'oreiller.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
