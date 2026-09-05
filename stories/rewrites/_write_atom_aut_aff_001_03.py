#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-03 — F-NAR-019. Nino, pique-nique de la pente. N1. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-03"
TITLE = "Le pique-nique de la pente"
CHARS = "Nino, maman"
SETTING = "chalet de montagne puis herbe de la pente"
FIL = (
    "Nino veut croquer le biscuit chaud sur la pente, tout de suite. "
    "Il part les bras pleins : la gourde tombe. Il refuse de foncer. "
    "L'éclat de marche libère la sangle. Le sac ferme. "
    "Le biscuit croque dans l'herbe, l'éclat pâle sur le rouge."
)
TICS = (
    "tout doux",
    "tout calme",
    "encore",
    "déjà",
    "merle",
    "miel",
    "aujourd'hui",
    "grain de miette",
    "éclat de pince",
    "grain de savon",
    "on va apprendre",
    "mission accomplie",
    "j'ai compris",
)
PROFILES = {
    "opening": {
        "rate": "medium",
        "wpm": 142,
        "speed": 0.98,
        "piper": 1.12,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 500,
        "sentence": 260,
        "energy": "warm",
        "contour": "storytelling",
        "noise": 0.36,
        "emphasis": "éclat de marche",
        "note": (
            "arc=installation; intention=ouvrir_le_monde; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le biscuit veut sortir tout de suite; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    },
    "clue": {
        "rate": "slow",
        "wpm": 120,
        "speed": 0.86,
        "piper": 1.27,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "soft",
        "db": -2,
        "pause": 700,
        "sentence": 320,
        "energy": "focused",
        "contour": "rising",
        "noise": 0.32,
        "emphasis": "sac",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=les affaires voyagent dans le sac; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "obstacle": {
        "rate": "medium",
        "wpm": 134,
        "speed": 0.93,
        "piper": 1.18,
        "pitch": "low",
        "pitchSsml": "-2st",
        "pitchTag": "low-pitch",
        "volume": "medium",
        "db": 0,
        "pause": 520,
        "sentence": 300,
        "energy": "tense",
        "contour": "dynamic",
        "noise": 0.34,
        "emphasis": "sangle",
        "note": (
            "arc=obstacle; intention=ralentir_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=l_eclat de marche tient la sangle; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "action": {
        "rate": "medium",
        "wpm": 146,
        "speed": 1.0,
        "piper": 1.10,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 420,
        "sentence": 250,
        "energy": "lively",
        "contour": "dynamic",
        "noise": 0.37,
        "emphasis": "biscuit",
        "note": (
            "arc=action; intention=mener_au_pique_nique; emotion=élan_retenu; intensite=2; "
            "destinataire=enfant; sous_texte=le biscuit attend dans le sac; "
            "tempo=vif; sourire=léger; respiration=courte"
        ),
    },
    "ending": {
        "rate": "slow",
        "wpm": 118,
        "speed": 0.85,
        "piper": 1.28,
        "pitch": "low",
        "pitchSsml": "-2st",
        "pitchTag": "low-pitch",
        "volume": "soft",
        "db": -3,
        "pause": 900,
        "sentence": 340,
        "energy": "calm",
        "contour": "falling",
        "noise": 0.31,
        "emphasis": "éclat de marche",
        "note": (
            "arc=retour; intention=refermer; emotion=fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_eclat de marche a voyagé sur le sac; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    },
}


def L(role: str, phrase: str) -> str:
    phrase = phrase.strip()
    if not phrase.endswith((".", "?", "!")):
        raise SystemExit(f"ponct: {phrase}")
    parts = re.findall(r"[^.?!]+[.?!]", phrase)
    if len(parts) != 1:
        raise SystemExit(f"plusieurs phrases: {phrase}")
    n = words(phrase)
    if n > 10:
        raise SystemExit(f"{n}>10: {phrase}")
    if n == 0:
        raise SystemExit(f"vide: {phrase}")
    low = phrase.lower()
    for tic in TICS:
        if tic in low:
            raise SystemExit(f"tic {tic}: {phrase}")
    return f"{role}|{phrase}"


def ssml(text: str, m: dict) -> str:
    body = html.escape(text, quote=False)
    if m.get("emphasis"):
        e = html.escape(m["emphasis"], quote=False)
        tagged = f'<emphasis level="moderate">{e}</emphasis>'
        body = body.replace(e, tagged, 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
    )


def xai(text: str, m: dict) -> str:
    body = text
    if m.get("emphasis"):
        e = m["emphasis"]
        body = body.replace(e, f"<emphasis>{e}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + tail).strip()


def apply_tts(src: dict, lines: list[str], sons: str, profile: str) -> dict:
    text, script = from_script(lines)
    m = dict(PROFILES[profile])
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
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = 0 if profile == "opening" else 200
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
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    return nc


SCRIPTS = {
    "CHK_T0000_P0000": [
        L("narrateur", "Dans le chalet, une casserole chuchote."),
        L("narrateur", "Le vent de la pente lui répond."),
        L("narrateur", "Il glisse sous la porte, frais."),
        L("narrateur", "Il touche la première marche."),
        L("narrateur", "Un éclat de marche brille, pâle."),
        L("narrateur", "Nino le voit, sans savoir."),
        L("narrateur", "L'herbe dehors sent le foin."),
        L("narrateur", "La maison de bois craque."),
        L("narrateur", "Ça sent le biscuit, tout chaud."),
        L("narrateur", "Une vapeur danse près du four."),
        L("narrateur", "Dehors, une pierre grise chauffe."),
        L("narrateur", "Un oiseau de montagne crie, haut."),
        L("maman", "Nino, le biscuit est prêt."),
        L("enfant-m", "On le mange dehors, tout de suite ?"),
        L("maman", "Oui, sur la pente."),
        L("maman", "Un pique-nique, tout petit."),
        L("narrateur", "En ce moment, Nino saisit le paquet."),
        L("narrateur", "Le papier est tiède sous les doigts."),
        L("enfant-m", "Je le porte, maman."),
        L("enfant-m", "Pas besoin du sac."),
        L("narrateur", "Il prend aussi la gourde verte."),
        L("narrateur", "Elle pique, trop froide."),
        L("enfant-m", "Aïe !"),
        L("narrateur", "Il court vers la porte, les bras pleins."),
        L("narrateur", "Le vent pousse le battant."),
        L("narrateur", "Le paquet glisse."),
        L("narrateur", "La gourde tombe sur le bois."),
        L("narrateur", "Patatras."),
        L("enfant-m", "Oh."),
        L("narrateur", "Le biscuit roule vers le seuil."),
        L("narrateur", "Nino le rattrape, les joues chaudes."),
        L("narrateur", "Le sourire de Nino disparaît."),
        L("narrateur", "Dans sa poitrine, ça se bouscule."),
        L("maman", "Tu voulais partir tout de suite ?"),
        L("enfant-m", "Le biscuit va refroidir."),
        L("narrateur", "Maman s'accroupit, à sa hauteur."),
        L("maman", "Où le biscuit voyage-t-il mieux ?"),
        L("enfant-m", "Dans mes mains."),
        L("narrateur", "Le papier se froisse, trop lâche."),
        L("narrateur", "Le sac rouge attend par terre."),
        L("narrateur", "La sangle est lisse, un peu froide."),
        L("enfant-m", "Il est rouge."),
        L("maman", "Oui, c'est le tien."),
        L("narrateur", "Nino pose le biscuit dedans."),
        L("narrateur", "Le papier se tait."),
        L("maman", "L'eau aussi."),
        L("narrateur", "Un linge à carreaux attend."),
        L("narrateur", "Nino l'enroule autour de l'eau."),
        L("enfant-m", "C'est moins froid."),
        L("narrateur", "Il glisse l'eau dans le sac."),
        L("enfant-m", "Où est le chapeau ?"),
        L("narrateur", "Le crochet du bas est vide."),
        L("narrateur", "Le chapeau est trop haut."),
    ],
    "CHK_T0000_P0000_Q0001": [
        L("narrateur", "Nino prépare le sac."),
        L("narrateur", "Où met-il les affaires ?"),
    ],
    "CHK_T0000_P0000_C0001": [
        L("narrateur", "Nino pousse une chaise vers le crochet."),
        L("narrateur", "La chaise glisse sur le bois."),
        L("narrateur", "Le chapeau penche, trop loin."),
        L("enfant-m", "Je n'arrive pas."),
        L("narrateur", "Ses épaules baissent."),
        L("maman", "Tu regardes, d'abord ?"),
        L("narrateur", "Nino refuse de foncer."),
        L("enfant-m", "J'attends."),
        L("narrateur", "Il pose un pied sur la marche."),
        L("narrateur", "L'éclat de marche accroche la sangle."),
        L("narrateur", "Nino tire, trop vite."),
        L("narrateur", "La sangle reste."),
        L("enfant-m", "Ça tient."),
        L("narrateur", "Maman se tait."),
        L("narrateur", "Nino observe le sac, puis la marche."),
        L("narrateur", "Le même éclat pâle, du début."),
        L("enfant-m", "C'est lui."),
        L("narrateur", "Il soulève la sangle, sans tirer."),
        L("narrateur", "La sangle passe."),
        L("narrateur", "Il prend le chapeau, mou, tiède."),
        L("narrateur", "Il le pose dans le sac."),
        L("enfant-m", "Il est dedans."),
        L("maman", "Merci, Nino."),
        L("maman", "La sangle est libre."),
        L("narrateur", "Nino appuie sur la fermeture."),
        L("narrateur", "Ça fait zzz."),
        L("narrateur", "Le sac rouge est fermé."),
        L("maman", "Le sac est prêt ?"),
        L("enfant-m", "Oui, maman."),
        L("narrateur", "Nino pose la main sur le rouge."),
        L("maman", "Le biscuit voyage avec nous."),
        L("enfant-m", "Dans le sac."),
        L("maman", "On met tes chaussures ?"),
        L("enfant-m", "Oui."),
    ],
    "CHK_T0000_P0000_END": [
        L("narrateur", "Nino enfile ses chaussures."),
        L("narrateur", "La semelle gratte le bois."),
        L("maman", "Tu as fini tes chaussures ?"),
        L("enfant-m", "Oui, maman."),
        L("narrateur", "Maman ouvre la porte."),
        L("narrateur", "L'air de la pente entre, frais."),
        L("narrateur", "L'herbe est un peu sèche."),
        L("narrateur", "Ils s'assoient près d'une pierre chaude."),
        L("enfant-m", "Le goûter, maintenant ?"),
        L("maman", "Oui, il est dans le sac."),
        L("narrateur", "Nino ouvre un tout petit peu."),
        L("narrateur", "Le papier fait un bruit fin."),
        L("narrateur", "Une fourmi passe dans l'herbe."),
        L("enfant-m", "Elle veut le biscuit ?"),
        L("maman", "Elle a son chemin."),
        L("maman", "Nous, le nôtre."),
        L("narrateur", "Nino sort le paquet."),
        L("narrateur", "Le biscuit est un peu chaud."),
        L("enfant-m", "Il sent bon."),
        L("maman", "Tu croques ?"),
        L("enfant-m", "Oui."),
    ],
    "CHK_T0000_P0000_END_F0001": [
        L("narrateur", "Nino croque le biscuit."),
        L("narrateur", "La croûte casse, toute légère."),
        L("enfant-m", "Il est chaud."),
        L("maman", "Comme le four, à l'instant."),
        L("narrateur", "Le sac rouge repose dans l'herbe."),
        L("narrateur", "Le vent de la pente passe."),
        L("narrateur", "La pierre grise chauffe sous la main."),
        L("narrateur", "Sur le rouge, un éclat de marche."),
        L("enfant-m", "Il a voyagé aussi."),
        L("maman", "Oui."),
        L("narrateur", "Le même, pâle, minuscule."),
    ],
}

SONS = {
    "CHK_T0000_P0000": "vent,casserole",
    "CHK_T0000_P0000_Q0001": "",
    "CHK_T0000_P0000_C0001": "zip",
    "CHK_T0000_P0000_END": "herbe,vent",
    "CHK_T0000_P0000_END_F0001": "",
}

PROFILE_FOR = {
    "CHK_T0000_P0000": "opening",
    "CHK_T0000_P0000_Q0001": "clue",
    "CHK_T0000_P0000_C0001": "obstacle",
    "CHK_T0000_P0000_END": "action",
    "CHK_T0000_P0000_END_F0001": "ending",
}

RELECTURE = """# ATOM-AUT.AFF.001-03 — Le pique-nique de la pente

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

- **Titre noyau :** *Le pique-nique de la pente*
- **Public :** N1 (≤ 10 mots/phrase)
- **Leçon :** AUT.AFF.001 — préparer le sac, vécue (bras pleins = chute ; le biscuit, l'eau et le chapeau voyagent dans le sac)
- **Personnages :** Nino, maman (dump)
- **Lieu :** chalet de montagne puis herbe de la pente (dump)
- **Indice unique :** éclat de marche (pas grain de savon / grain de miette / éclat de pince)

## Promesse narrative

Nino veut croquer le biscuit chaud **maintenant**, sur la pente. Il part les bras pleins, sans sac : le vent pousse le battant, la gourde tombe, le sourire disparaît. Maman s'accroupit, pose une question, ne dicte pas. Nino pose biscuit et eau dans le sac rouge. Le chapeau est trop haut : la chaise glisse. Il refuse de foncer. Sur la marche, l'éclat pâle du début accroche la sangle. Tirer échoue. Il soulève. Merci vécu. Zip. Sur l'herbe, le biscuit croque. L'éclat de marche a voyagé sur le rouge.

## Vécu

Impatience (tout de suite, bras pleins), découragement (épaules, « je n'arrive pas »), fierté calme (sangle libre, main sur le rouge). Un « en ce moment ». Un merci de maman (la sangle est libre). Question d'écoute : le sac. Q moteur inchangée.

## Vu et corrigé

F-NAR-019. Monde du dump conservé, ≠ four du village ≠ cour de Sarah. Tics « encore / déjà / tout doux / tout calme / merle / miel / aujourd'hui » absents. Première idée échoue. Choix de Nino (ne pas foncer) change l'action. Fin paie l'éclat de marche. TTS par chunk : `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration), `text_ssml`, `text_xai_tags`, piper variable. `slow` réservé à la question et à la fin. `check()` N1 OK. Pas apply. Pas git. Pas audio.

## Direction vocale

Ouverture chaude, question lente, obstacle plus grave, pente plus vive, fin posée. Emphasis : éclat de marche / sac / sangle / biscuit.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
"""


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in SCRIPTS]
    extra = set(SCRIPTS) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} missing={missing} extra={extra}")
    out_chunks = []
    piper_vals = set()
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind_src = c.get("kind")
        nc = apply_tts(c, SCRIPTS[cid], SONS[cid], PROFILE_FOR[cid])
        if nc.get("kind") != kind_src:
            raise SystemExit(f"kind changé {cid}")
        piper_vals.add(nc["length_scale_piper"])
        out_chunks.append(nc)
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = out_chunks
    check(SID, out["age_band"], out["chunks"])
    joined = "\n".join(c["script"] for c in out_chunks).lower()
    for tic in TICS:
        if tic in joined:
            raise SystemExit(f"{SID} extra interdit: {tic}")
    if "éclat de marche" not in joined:
        raise SystemExit("indice éclat de marche manquant")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "refuse de foncer" not in joined:
        raise SystemExit("refuse de foncer manquant")
    for c in out_chunks:
        if not c.get("notes") or "arc=" not in c["notes"]:
            raise SystemExit(f"notes manquantes {c['chunk_id']}")
        if not c.get("text_xai_tags") or c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"xai trop plat {c['chunk_id']}")
        if "<speak>" not in (c.get("text_ssml") or ""):
            raise SystemExit(f"ssml plat {c['chunk_id']}")
    nwords = sum(words(c["text"]) for c in out_chunks)
    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / SID / "RELECTURE.md").write_text(RELECTURE, encoding="utf-8")
    print(f"wrote {path} mots={nwords} piper={sorted(piper_vals)}")


if __name__ == "__main__":
    main()
