#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-05 — L'escargot du jardin (F-NAR-019, N1, AUT.AFF.001)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-05"
N1 = 10
TITLE = "L'escargot du jardin"
CHILD = "enfant-m"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|encore|déjà|deja)\b",
    re.I,
)
CLUE_BAD = (
    "grain de miette",
    "éclat de pince",
    "grain de foin",
    "éclat de corde",
    "merle",
    "couleur de miel",
    "j'ai compris",
    "mission accomplie",
    "aujourd'hui,",
    "gouttes au bord",
    "on dirait que notre mission",
    "avec un détour que personne",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de feuille",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=2; destinataire=enfant; sous_texte=le_grain_brille_sur_la_feuille_du_seau; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sac",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=la_loupe_va_dans_le_sac; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="grain de feuille",
        note="arc=confirmation; intention=relancer; emotion=fierté_calme; intensite=1; destinataire=enfant; sous_texte=il_a_refusé_de_foncer; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de feuille",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le_grain_du_début_paie_sous_la_feuille; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de feuille",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_loupe_porte_une_trace_d_eau; tempo=posé; sourire=léger; respiration=ample",
    ),
}

Q_FIELDS = {
    "expected_answer": "le sac",
    "accepted_examples": "le sac | dans le sac | il met | elle met | mettre",
    "retry_prompt": "Il met les affaires dans le sac. Où les met Raphaël ?",
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
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
        for bad in CLUE_BAD:
            if bad in low:
                raise SystemExit(f"indice/refrain {bad}: {ph}")
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
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m.get("emphasis") or ""
    nc["pause_before_ms"] = extra.get("pause_before_ms", 0)
    nc["pause_after_ms"] = m["pause"]
    nc["pause_sentence_ms"] = m["sentence"]
    nc["style_energy"] = m["energy"]
    nc["style_contour"] = m["contour"]
    nc["noise_scale_piper"] = m["noise"]
    nc["kokoro_speed"] = m["speed"]
    nc["melo_speed"] = m["speed"]
    nc["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    nc["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    nc["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    nc["notes"] = extra.get("notes", m["note"])
    nc["night_policy"] = extra.get("night_policy", "play")
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


SCRIPTS = {
    "CHK_T0000_P0000": [
        "narrateur|La vapeur de la tasse dessine un rond.",
        "narrateur|Sur la vitre grise, le rond tremble.",
        "narrateur|À travers, le seau jaune apparaît.",
        "narrateur|Une feuille collée tapote au bord.",
        "narrateur|Un grain de feuille brille dessus.",
        "narrateur|Raphaël colle son nez à la vitre.",
        "narrateur|Le jardin sent la terre mouillée.",
        "narrateur|La dalle du seau luit, pâle.",
        "narrateur|Papa ouvre le tiroir de laine.",
        "narrateur|Ça fait un petit bruit sourd.",
        "narrateur|La maison sent la laine et le thé.",
        "narrateur|Une botte penche près de la porte.",
        "papa|Raphaël, tu vois le grain dehors ?",
        "enfant-m|Oui, papa.",
        "enfant-m|Je veux l'escargot maintenant.",
        "papa|Sa trace d'argent va sécher.",
        "papa|On y va, avec le sac.",
        "narrateur|En ce moment, Raphaël saisit le sac.",
        "narrateur|Le sac vert est par terre.",
        "narrateur|Une loupe ronde attend dans la poche.",
        "enfant-m|Il est vert, papa.",
        "papa|Oui, c'est le tien.",
        "papa|Prends la loupe, pour ses cornes.",
        "narrateur|Raphaël prend la loupe ronde.",
        "narrateur|Le verre est froid sous le doigt.",
        "narrateur|Le bord fait un petit clic.",
        "enfant-m|Vite, il va partir.",
        "narrateur|Raphaël tape du pied, impatient.",
        "narrateur|Il pousse la loupe dans le sac.",
        "narrateur|Il tire le zip d'un coup.",
        "narrateur|Le zip se coince, dur.",
        "enfant-m|Ça ne veut pas, papa.",
        "narrateur|La loupe bascule et glisse.",
        "narrateur|Raphaël la rattrape contre sa poitrine.",
        "narrateur|Son sourire disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent.",
        "narrateur|Le cœur de Raphaël bat plus fort.",
        "narrateur|Papa s'accroupit à sa hauteur.",
        "papa|Tu aides le zip ?",
    ],
    "CHK_T0000_P0000_Q0001": [
        "narrateur|La loupe attend près du zip.",
        "narrateur|Raphaël prépare le sac.",
        "narrateur|Où met-il les affaires ?",
    ],
    "CHK_T0000_P0000_C0001": [
        "narrateur|Raphaël refuse de foncer.",
        "narrateur|Il pose la loupe sur le bois.",
        "narrateur|Papa attend, sans parler.",
        "narrateur|Il observe la loupe, puis le zip.",
        "narrateur|Le seau tape un petit tic.",
        "narrateur|Il regarde les dents du zip.",
        "narrateur|Un grain de feuille est coincé.",
        "enfant-m|C'est le grain de la feuille.",
        "narrateur|Il le soulève du bout de l'ongle.",
        "narrateur|Le zip se libère, lisse.",
        "narrateur|Il glisse la loupe dans le sac.",
        "narrateur|Le verre rejoint le fond.",
        "enfant-m|Elle est au chaud.",
        "papa|Merci, Raphaël.",
        "narrateur|Raphaël ferme le sac.",
        "narrateur|Ça fait zzz, bas.",
        "narrateur|Le sac vert est fermé.",
        "papa|Le sac est prêt ?",
        "enfant-m|Oui, papa.",
        "narrateur|Il pose la main sur le tissu.",
        "narrateur|Le vert est un peu sombre.",
        "narrateur|La vitre montre le seau, dehors.",
        "papa|On met le manteau ?",
        "enfant-m|Oui.",
    ],
    "CHK_T0000_P0000_END": [
        "narrateur|Raphaël enfile le manteau.",
        "narrateur|Le manteau sent la pluie.",
        "papa|Tu as fini ton manteau ?",
        "enfant-m|Oui, papa.",
        "papa|On ouvre la porte.",
        "narrateur|Papa ouvre la porte.",
        "narrateur|L'air sent la terre mouillée.",
        "narrateur|Le seau garde sa feuille collée.",
        "narrateur|Une flaque fait un petit cercle.",
        "enfant-m|Vite, sous toutes les feuilles.",
        "narrateur|Il avance la main trop vite.",
        "narrateur|La feuille glisse, trop loin.",
        "enfant-m|Il n'est pas là.",
        "narrateur|Raphaël s'arrête net.",
        "narrateur|Toutes les feuilles se ressemblent.",
        "narrateur|Cette fois, il refuse de foncer.",
        "narrateur|Il cherche le grain de feuille.",
        "narrateur|Le grain brille sur la feuille du seau.",
        "enfant-m|C'est lui, papa.",
        "narrateur|Ils s'accroupissent près du seau.",
        "narrateur|La terre est froide sous les genoux.",
        "narrateur|Il soulève le bord, sans brusquer.",
        "narrateur|Sous la feuille, un escargot avance.",
        "narrateur|Sa coquille est brillante, un peu brune.",
        "enfant-m|Il est là.",
        "papa|Tu l'as trouvé, sans foncer.",
        "narrateur|Une goutte tombe dans la flaque.",
        "narrateur|Le cercle grandit un peu.",
        "papa|On le regarde avec la loupe ?",
        "enfant-m|Oui.",
    ],
    "CHK_T0000_P0000_END_F0001": [
        "narrateur|Raphaël sort la loupe du sac.",
        "narrateur|Le verre encadre deux cornes prudentes.",
        "enfant-m|Il avance.",
        "papa|Oui, tu l'as trouvé.",
        "narrateur|Le sac vert repose près du seau.",
        "narrateur|La loupe garde une trace d'eau.",
        "narrateur|Le grain de feuille brille toujours.",
        "narrateur|La flaque ronde brille, elle aussi.",
    ],
}

SONS = {
    "CHK_T0000_P0000": "pluie,tasse,tiroir",
    "CHK_T0000_P0000_Q0001": "",
    "CHK_T0000_P0000_C0001": "zip,seau",
    "CHK_T0000_P0000_END": "porte,pluie,flaque",
    "CHK_T0000_P0000_END_F0001": "",
}

KIND_PROFILE = {
    "CHK_T0000_P0000": "opening",
    "CHK_T0000_P0000_Q0001": "clue",
    "CHK_T0000_P0000_C0001": "confirm",
    "CHK_T0000_P0000_END": "resolution",
    "CHK_T0000_P0000_END_F0001": "ending",
}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in SCRIPTS]
    extra = set(SCRIPTS) - set(by_src)
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")
    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        extra = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra["fields"] = dict(Q_FIELDS)
            extra["pause_before_ms"] = 200
        elif cid != "CHK_T0000_P0000":
            extra["pause_before_ms"] = 200
        chunks.append(
            voice(by_src[cid], SCRIPTS[cid], KIND_PROFILE[cid], SONS.get(cid, ""), extra)
        )
    out = dict(src)
    out["fil_rouge"] = (
        "Raphaël veut voir l'escargot du coin du seau avant que sa trace sèche. "
        "Il fonce, le zip se coince sur un grain de feuille. "
        "Il refuse de tirer, glisse la loupe dans le sac, "
        "retrouve le même grain sous la feuille du seau."
    )
    out["title"] = TITLE
    out["characters"] = "Raphaël, papa"
    out["setting"] = "maison puis le coin du seau, jardin après la pluie"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    nwords = sum(words(c["text"]) for c in chunks)
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Raphaël veut l'escargot **maintenant**, avant que la trace d'argent sèche. "
        "Première idée : pousser la loupe et tirer le zip d'un coup. La loupe bascule. "
        "Il refuse de foncer, lève le grain de feuille coincé, glisse la loupe **dans le sac**. "
        "Dehors, toutes les feuilles se ressemblent ; le grain du début paie sous la feuille du seau. "
        "Papa dit merci quand le zip se libère. La loupe garde une trace d'eau.\n\n"
        "## Vu et corrigé\n"
        "- Monde du dump (maison, vitre, tasse, jardin après la pluie) ; coin nommé : la dalle du seau.\n"
        "- Objet : loupe ronde (froid, clic, mission : voir les cornes).\n"
        "- Indice unique : grain de feuille (ouverture, zip, feuille du seau, fin). "
        "Pas grain de miette / éclat de pince / grain de foin / éclat de corde.\n"
        "- Leçon AUT.AFF.001 vécue (la loupe va dans le sac), jamais dite.\n"
        "- N1 ≤ 10. Un « en ce moment ». Un merci vécu. Question d'écoute conservée.\n"
        "- TTS notes + ssml + xai + piper par chunk. Tics encore/déjà/tout doux absents.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
