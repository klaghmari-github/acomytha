#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-01 — F-NAR-019. La nappe à carreaux. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-01"
N1 = 10
TITLE = "La nappe à carreaux"
FIL = (
    "La vanille arrive dans le salon, avant le gâteau. Sur un carreau rouge, "
    "un éclat de nappe brille. Raphaël veut la tour haute, maintenant, avec "
    "le doudou. Un cube glisse : le doudou disparaît. Il cherche sous la "
    "nappe, sous le coussin, puis prend toute la pile : les cubes "
    "s'éparpillent. Il refuse de foncer, pose un cube, retrouve le doudou. "
    "Sur la nappe ouverte, l'éclat de nappe tient au carreau du doudou."
)
CHARS = "Raphaël, papa, maman"
SETTING = "cuisine à la vanille, salon, nappe à carreaux, après-midi du gâteau"
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
    "grain de carotte",
    "grain de lavande",
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
        emphasis="éclat de nappe",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_tour_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="doudou",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_doudou_est_sous_les_cubes; "
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
        emphasis="nappe",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_tirer_la_nappe; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de nappe",
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
    "narrateur|La vanille arrive dans le salon, avant le gâteau.",
    "narrateur|Un carré de buée s'ouvre sur la vitre.",
    "narrateur|La cuillère en bois tape dans le bol.",
    "papa|Le gâteau est bientôt prêt.",
    "maman|Il sent bon, papa.",
    "narrateur|Dans le salon, le tapis est épais.",
    "narrateur|Une nappe à carreaux attend, pliée.",
    "narrateur|Elle repose sur la chaise.",
    "narrateur|Sur un carreau rouge, un éclat de nappe brille.",
    "enfant-m|Il est tout petit, maman.",
    "maman|C'est un éclat de nappe.",
    "narrateur|Le tissu sent un peu le savon.",
    "papa|Raphaël, tu sens le gâteau ?",
    "enfant-m|Oui, papa.",
    "enfant-m|Je veux la tour, maintenant !",
    "maman|Pendant que le gâteau refroidit ?",
    "enfant-m|Oui, une tour haute.",
    "narrateur|En ce moment, Raphaël saisit un cube.",
    "narrateur|Le cube vert est lisse, un peu froid.",
    "narrateur|Il le pose au milieu du tapis.",
    "narrateur|Ça fait clic, tout petit.",
    "narrateur|Puis un cube jaune.",
    "narrateur|Ça fait clic, contre le vert.",
    "enfant-m|Le cube du haut, c'est le gâteau.",
    "maman|Un gâteau de cubes !",
    "narrateur|Le doudou gris est au pied.",
    "narrateur|Raphaël l'assoit contre la tour.",
    "enfant-m|Toi, tu goûtes avec nous.",
    "papa|Elle est belle, ta tour.",
    "narrateur|Raphaël veut un cube de plus.",
    "narrateur|Il le pose trop vite.",
    "narrateur|Un cube jaune glisse.",
    "narrateur|La tour penche.",
    "narrateur|Trois cubes tombent sur le doudou.",
    "enfant-m|Oh.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|Où est mon doudou ?",
    "maman|Sous la nappe, peut-être ?",
    "narrateur|Il va vers la chaise.",
    "narrateur|Il soulève un coin du tissu.",
    "narrateur|L'éclat de nappe tremble, puis tient.",
    "narrateur|Pas de tissu gris.",
    "enfant-m|Il n'est pas là.",
    "papa|Près du canapé ?",
    "narrateur|Sa main passe sous le coussin.",
    "narrateur|Le coussin est moelleux.",
    "narrateur|Le doudou n'est pas là.",
    "enfant-m|Il est perdu.",
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
    "narrateur|Raphaël cherche son doudou.",
    "narrateur|Où est-il ?",
]

C0001 = [
    "narrateur|Raphaël refuse de prendre toute la pile.",
    "narrateur|Il pose un genou au tapis.",
    "narrateur|Un cube vert reste près de sa main.",
    "enfant-m|Je le mets tout seul.",
    "narrateur|Il glisse le cube dans la caisse.",
    "narrateur|Toc.",
    "narrateur|Le bois sent un peu la forêt.",
    "maman|Tu regardes bien dessous ?",
    "enfant-m|Oui, maman.",
    "narrateur|La tour devient plus petite.",
    "narrateur|Un bout de tapis reparaît.",
    "narrateur|Le cube jaune va dans la caisse.",
    "narrateur|Toc.",
    "enfant-m|Je sors le reste, d'un coup !",
    "narrateur|Il tire trop fort sur un cube bas.",
    "narrateur|Deux cubes retombent, comme un toit.",
    "enfant-m|Oh.",
    "narrateur|Il ne reprend pas trop vite.",
    "narrateur|Il écoute le salon, un instant.",
    "narrateur|Sur la chaise, l'éclat de nappe brille.",
    "enfant-m|Il est là.",
    "narrateur|Raphaël refuse de foncer.",
    "narrateur|Il écarte un cube, lentement.",
    "narrateur|Un coin de tissu gris.",
    "enfant-m|Mon doudou !",
    "narrateur|Le doudou était sous la tour.",
    "narrateur|Il sent le tapis, un peu chaud.",
    "narrateur|Raphaël le serre contre sa joue.",
    "papa|Merci, Raphaël.",
    "enfant-m|Il était dessous.",
    "narrateur|La caisse a presque tous les cubes.",
    "narrateur|Le tapis est libre, au milieu.",
    "maman|La nappe peut s'ouvrir ?",
    "enfant-m|Oui, maman.",
    "narrateur|Raphaël pose la main sur le doudou.",
    "narrateur|Le tissu est un peu rêche.",
]

END = [
    "papa|On déplie la nappe ?",
    "narrateur|Maman déplie la nappe à carreaux.",
    "narrateur|Raphaël tient un coin.",
    "narrateur|Les carreaux sont rouges et blancs.",
    "narrateur|Un cube oublié accroche le tissu.",
    "enfant-m|Je tire !",
    "narrateur|Raphaël s'arrête.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il recule le cube, lentement.",
    "narrateur|La nappe se pose, plate.",
    "papa|Le vrai gâteau peut s'asseoir.",
    "narrateur|Papa pose le plat chaud.",
    "narrateur|La vanille remplit le salon.",
    "enfant-m|Le doudou a un carreau.",
    "maman|Oui, le carreau rouge.",
    "narrateur|L'éclat de nappe tremble sur le rouge.",
    "papa|Tu veux un peu d'eau ?",
    "enfant-m|Oui, papa.",
    "narrateur|L'eau fait un petit bruit.",
    "narrateur|Raphaël casse un bout tiède.",
    "narrateur|La miette fond un peu.",
    "enfant-m|C'est bon, papa.",
    "maman|On est bien, ici.",
    "narrateur|Le doudou reste contre lui.",
]

FIN = [
    "narrateur|Ils s'assoient près de la nappe tiède.",
    "narrateur|La chaleur touche les joues de Raphaël.",
    "enfant-m|Le gâteau est là.",
    "maman|Oui, tout chaud.",
    "narrateur|Le doudou a un tout petit bout.",
    "enfant-m|Comme l'éclat de nappe, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, sur le carreau rouge.",
    "narrateur|Raphaël glisse le doudou sans se presser.",
    "narrateur|Le tissu repose contre sa hanche.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est chaud.",
    "narrateur|La vanille reste dans l'air.",
    "narrateur|L'éclat de nappe tient sur le carreau.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "cuillère,cubes",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "le doudou",
                    "accepted_examples": (
                        "le doudou | doudou | sous la tour | sous les cubes "
                        "| dessous"
                    ),
                    "retry_prompt": "Il cherche sous les cubes. Où est le doudou ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "caisse,bois",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "nappe,plat",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "gâteau,vanille",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de nappe" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de nappe" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
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
        "- **Leçon :** AUT.RAN.001 — ranger (vécue : doudou sous les cubes)\n"
        "- **Personnages :** Raphaël, papa, maman\n"
        "- **Lieu :** cuisine à la vanille, salon, nappe à carreaux, "
        "après-midi du gâteau\n"
        "- **Indice unique :** éclat de nappe (carreau rouge plié → carreau "
        "du doudou)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La vanille arrive dans le salon avant le gâteau. Un carré de buée "
        "s'ouvre sur la vitre. Sur un carreau rouge, un éclat de nappe "
        "brille. Raphaël veut la tour haute **maintenant**, avec le doudou "
        "invité. Il pose trop vite : un cube glisse, la tour tombe sur le "
        "doudou. Première idée : sous la nappe, sous le coussin. Rien. Il "
        "prend toute la pile d'un coup : les cubes s'éparpillent. Sourire "
        "parti, épaules basses. Papa se baisse. Raphaël refuse de foncer, "
        "pose un cube, tire trop fort : deux cubes retombent. Il écoute, "
        "voit l'éclat, écarte un cube. Le doudou était dessous. Merci vécu. "
        "Un cube accroche la nappe : il recule le cube. Sur la nappe "
        "ouverte, l'éclat tient au carreau du doudou. Les joues sont "
        "chaudes.\n\n"
        "## Vécu\n\n"
        "Raphaël veut la tour **maintenant**. Impatience, puis épaules qui "
        "tombent quand la pile résiste. Papa se baisse, pose une question, "
        "ne récite pas la règle. Raphaël agit : genou au tapis, cube dans "
        "la caisse, doudou retrouvé. Merci vécu après le doudou. Fin : "
        "l'éclat du début tient sur le carreau.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (vanille avant le gâteau, buée, éclat), pas "
        "« joue au salon ».\n"
        "- Monde du dump (cuisine vanille, salon, nappe, gâteau), distinct "
        "de AFF.003 (parc, seau).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Leçon non dite : le doudou reparaît quand les cubes vont dans "
        "la caisse. Pas de morale, pas « on va ranger ».\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
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
