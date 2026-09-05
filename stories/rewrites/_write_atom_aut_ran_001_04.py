#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-04 — F-NAR-019. La cabane sous la table. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-04"
N1 = 10
TITLE = "La cabane sous la table"
FIL = (
    "Le torchon glisse. Une cuillère tinte. Au pied de la chaise, "
    "un éclat d'ombre brille. Sarah veut sa cabane sous la table, "
    "maintenant. Elle pousse le coussin d'un coup : une voiture touche "
    "son genou, le doudou disparaît. Première idée ratée. Elle refuse "
    "de foncer, pose les voitures dans la caisse. L'éclat d'ombre "
    "montre le rose. Merci vécu. Au plafond de nappe, l'éclat d'ombre dore."
)
CHARS = "Sarah, papa, maman"
SETTING = "salon après le déjeuner, nappe savon, dessous de table, caisse bleue"
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
    "grain de pomme",
    "grain de sable",
    "grain de lessive",
    "grain de toile",
    "grain de laine",
    "grain de grelot",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'écorce",
    "éclat de laine",
    "éclat de carreau",
    "éclat de grain",
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
    "terre grise",
    "ancre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat d'ombre",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_cabane_maintenant; "
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
            "intensite=1; destinataire=enfant; sous_texte=le_doudou_est_dessous; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat d'ombre",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_de_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="cabane",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; sous_texte=la_cabane_prend_place; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat d'ombre",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_éclat_du_pied_dore_la_nappe; "
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
        found = TIC_WORDS.search(low)
        if found:
            raise SystemExit(f"tic {found.group(0)!r}: {ph}")
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
    "narrateur|Le torchon glisse sur le bois.",
    "narrateur|Ça sent le savon, tiède.",
    "papa|J'essuie la table, Sarah.",
    "narrateur|Une cuillère tinte dans un verre.",
    "narrateur|Au pied de la chaise, un éclat d'ombre brille.",
    "enfant-f|Il est petit, papa.",
    "papa|C'est l'ombre de la chaise.",
    "narrateur|L'éclat d'ombre coupe le tapis.",
    "narrateur|La nappe sent le savon.",
    "narrateur|Un coin de nappe tombe vers le tapis.",
    "maman|Je prends le coussin.",
    "narrateur|Sous la table, il fait sombre.",
    "narrateur|Sarah connaît ce dessous de table.",
    "narrateur|Un détail paraît nouveau, là.",
    "narrateur|L'éclat tremble sur le pied.",
    "narrateur|En ce moment, Sarah glisse dessous.",
    "enfant-f|Je veux ma cabane, maintenant.",
    "papa|Maintenant ?",
    "enfant-f|Oui, tout de suite.",
    "maman|Tu la veux sous la table ?",
    "enfant-f|Oui, avec le coussin.",
    "narrateur|Ses genoux trouvent le tapis.",
    "narrateur|Le tapis est un peu froid.",
    "narrateur|Des voitures bleues attendent.",
    "narrateur|Elles sont lisses, un peu froides.",
    "enfant-f|Elles roulent, papa.",
    "papa|Elles roulent dans l'ombre.",
    "narrateur|Sarah pousse une voiture.",
    "narrateur|Vroom.",
    "narrateur|Puis une autre.",
    "narrateur|Vroom.",
    "narrateur|Elle aligne trois voitures bleues.",
    "narrateur|Les roues sont froides sous le doigt.",
    "maman|C'est un parking ?",
    "enfant-f|Oui, sous la table.",
    "narrateur|Le doudou rose est près d'elle.",
    "enfant-f|Toi, tu restes dans la cabane.",
    "narrateur|Sarah le pose contre un pied.",
    "narrateur|Une voiture glisse vers lui.",
    "narrateur|Une deuxième le recouvre.",
    "narrateur|Le rose disparaît sous le bleu.",
    "enfant-f|Après, c'est ma cabane.",
    "maman|Avec le coussin ?",
    "enfant-f|Oui, une cabane.",
    "narrateur|Maman tend le coussin.",
    "narrateur|Il est moelleux, un peu lourd.",
    "narrateur|Sarah veut le glisser dessous.",
    "narrateur|Elle pousse fort, d'un coup.",
    "narrateur|Une voiture touche son genou.",
    "enfant-f|Aïe.",
    "papa|La voiture est là.",
    "narrateur|Le sourire de Sarah disparaît.",
    "narrateur|Ses épaules tombent un peu.",
    "enfant-f|Où est mon doudou ?",
    "maman|Sur la chaise, peut-être ?",
    "narrateur|Sarah sort la tête.",
    "narrateur|La chaise est vide.",
    "enfant-f|Dans le coussin ?",
    "narrateur|Elle fouille le tissu.",
    "narrateur|Rien.",
    "enfant-f|Il est perdu.",
    "narrateur|Ça serre, dans son ventre.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu regardes sous les voitures ?",
    "enfant-f|Je veux voir dessous.",
    "narrateur|Sarah prend une voiture bleue.",
    "narrateur|Elle la pose dans la caisse.",
    "narrateur|Clac.",
]

Q0001 = [
    "narrateur|Sarah cherche son doudou.",
    "narrateur|Où est-il ?",
]

C0001 = [
    "narrateur|Une deuxième voiture va dans la caisse.",
    "narrateur|Clac.",
    "maman|Tu regardes bien sous les roues ?",
    "enfant-f|Oui, maman.",
    "narrateur|Un bout de tapis reparaît.",
    "narrateur|Sarah glisse la troisième.",
    "narrateur|Clac.",
    "narrateur|Un coin de tissu rose.",
    "enfant-f|Je le prends, d'un coup !",
    "narrateur|Elle tire trop fort.",
    "narrateur|Les voitures retombent dessus.",
    "enfant-f|Oh.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Sarah recule d'un pas.",
    "enfant-f|Je ne fonce pas.",
    "narrateur|Elle refuse de tirer plus fort.",
    "narrateur|Personne ne dit la réponse.",
    "narrateur|Sarah observe les voitures, un instant.",
    "narrateur|Sous le pied, l'éclat d'ombre brille.",
    "enfant-f|Il montre le doudou.",
    "narrateur|Elle pose un genou au sol.",
    "narrateur|Elle sort la dernière, sans se presser.",
    "narrateur|Clac.",
    "narrateur|Le tapis reparaît, rose au milieu.",
    "enfant-f|Mon doudou !",
    "narrateur|Le doudou était sous les voitures.",
    "narrateur|Il sent le savon de la nappe.",
    "narrateur|Sarah le serre contre sa joue.",
    "narrateur|Le tissu est chaud, un peu plat.",
    "papa|Merci, tu l'as trouvé.",
    "maman|Te voilà, petit.",
    "enfant-f|Il était dessous.",
    "narrateur|La caisse bleue est presque pleine.",
    "narrateur|Sous la table, le tapis est libre.",
    "narrateur|L'ombre de la chaise reste là.",
]

END = [
    "papa|On met le coussin ?",
    "narrateur|Sarah glisse le coussin sous la table.",
    "narrateur|Le coussin est moelleux.",
    "enfant-f|C'est ma cabane.",
    "maman|Une cabane pour toi.",
    "narrateur|Elle s'assoit, le doudou sur les genoux.",
    "narrateur|La nappe fait un plafond.",
    "papa|On frappe avant d'entrer ?",
    "enfant-f|Toc toc.",
    "papa|On peut entrer ?",
    "enfant-f|Oui, papa.",
    "narrateur|Papa se penche un peu.",
    "narrateur|L'ombre sent le savon.",
    "maman|Tu veux un peu d'eau ?",
    "enfant-f|Oui, maman.",
    "narrateur|Sarah boit une gorgée.",
    "narrateur|L'eau est fraîche, un peu.",
    "narrateur|Le doudou reste contre elle.",
    "narrateur|Une ligne claire coupe le sol.",
    "enfant-f|On est bien, ici.",
    "papa|Oui, très bien.",
    "narrateur|Sarah pose la main sur la nappe.",
    "narrateur|Le tissu est un peu humide.",
    "enfant-f|On entend la cuillère ?",
    "papa|Elle est loin, maintenant.",
    "narrateur|Sarah écoute.",
    "narrateur|La maison est tranquille.",
]

FIN = [
    "enfant-f|Le doudou est dans la cabane.",
    "maman|Toi aussi.",
    "papa|Tu le serres bien ?",
    "enfant-f|Oui, papa.",
    "narrateur|La nappe sent le savon.",
    "narrateur|Au plafond, un éclat d'ombre brille.",
    "enfant-f|Comme au pied de la chaise !",
    "papa|Tu le vois, toi ?",
    "enfant-f|Oui, il est là.",
    "narrateur|Sarah le montre du doigt.",
    "enfant-f|Ma cabane est prête.",
    "maman|Elle te va bien.",
    "narrateur|Le savon reste dans l'air.",
    "narrateur|L'éclat d'ombre dore la nappe.",
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
        raise SystemExit(f"{SID} chunks inattendus missing={missing} extra={extra}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "torchon,cuillere,voitures",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "le doudou",
                    "accepted_examples": (
                        "le doudou | doudou | sous les voitures | dessous | sous les roues"
                    ),
                    "retry_prompt": "Elle cherche sous les voitures. Où est le doudou ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "caisse,voitures",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "coussin,toc",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "nappe",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat d'ombre" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat d'ombre" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "je ne fonce pas" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")
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
        "- **Leçon :** AUT.RAN.001 — retrouver en mettant les jouets dans la caisse (vécue, non dite)\n"
        "- **Personnages :** Sarah, papa, maman\n"
        "- **Lieu :** salon après le déjeuner, nappe savon, dessous de table, caisse bleue\n"
        "- **Indice unique :** éclat d'ombre (pied de chaise → plafond de nappe)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le torchon glisse sur le bois. Une cuillère tinte. Au pied de la "
        "chaise, un éclat d'ombre brille. Sarah connaît ce dessous de table ; "
        "le détail paraît nouveau. Elle veut sa cabane **maintenant**, avec le "
        "coussin. Les voitures bleues font un parking. Le doudou rose va contre "
        "un pied. Première idée : pousser le coussin d'un coup. Une voiture "
        "touche son genou. Le doudou disparaît. Chaise vide, coussin vide. "
        "Épaules qui tombent. Papa se baisse. Elle pose une voiture dans la "
        "caisse. Question : où est le doudou ? Deuxième ruse : tirer le rose "
        "d'un coup, les voitures retombent. Elle refuse de foncer. L'éclat "
        "d'ombre montre le dessous. Une dernière, sans se presser. Merci vécu. "
        "Coussin, nappe-plafond, toc toc. Au plafond, l'éclat d'ombre dore.\n\n"
        "## Vécu\n\n"
        "Sarah veut la cabane **maintenant**. Impatience, puis épaules qui "
        "tombent quand le doudou manque. Papa se baisse, pose une question, "
        "ne récite pas la règle. Sarah agit : voitures dans la caisse, genou "
        "au sol, doudou retrouvé, cabane tenue. Merci vécu après le doudou. "
        "Fin : l'éclat du pied de chaise dore la nappe.\n\n"
        "## Vu et corrigé\n\n"
        "- Monde du dump (salon, nappe savon, après déjeuner, Sarah). "
        "Pas nappe à carreaux, pas cacao Nina, pas pain Amir.\n"
        "- Ouverture inventée (torchon, cuillère, éclat d'ombre), pas « joue au salon ».\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Leçon non dite : elle met les voitures dans la caisse pour voir. Pas de morale.\n"
        "- Merci vécu. Question d'adulte. Un « en ce moment ».\n"
        "- Indice unique : éclat d'ombre. Pas grain de *, pas éclats bannis.\n"
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
