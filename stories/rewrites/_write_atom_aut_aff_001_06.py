#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-06 — La pomme du marché (F-NAR-019, N2, AUT.AFF.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-06"
TITLE = "La pomme du marché"
N2 = LIMITS["N2"]
CHARS = "Nina, papa, maman"
SETTING = "cuisine puis hall du marché"
FIL = (
    "Derrière la vitre floue, les caisses râpent le pavé. Un éclat de "
    "caisse cligne sur le verre. Nina veut une pomme du hall, maintenant, "
    "dans son sac. Elle jette tout d'un coup : la cuillère, le zip qui mord. "
    "Elle refuse de forcer, range, trouve le chapeau. Au hall, la pomme "
    "roule. Elle refuse de foncer, retrouve l'éclat. La pomme paie le début."
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
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "trait de craie",
    "pull bleu",
    "deux pommes",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de caisse",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_pomme_maintenant; "
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
            "intensite=1; destinataire=enfant; sous_texte=les_affaires_vont_dans_le_sac; "
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
            "destinataire=enfant; sous_texte=elle_prépare_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de caisse",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de caisse",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_la_vitre_est_sur_la_caisse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "le sac",
    "accepted_examples": "le sac | dans le sac | il met | elle met | mettre",
    "retry_prompt": "Elle met les affaires dans le sac. Où les met Nina ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "bouilloire,caisses,vitre",
        [
            "narrateur|Derrière la vitre floue, les caisses râpent le pavé.",
            "narrateur|Même ici, ça sent la pomme du hall.",
            "narrateur|Nina connaît cette cuisine, ses recoins.",
            "narrateur|La bouilloire chante, petite.",
            "narrateur|Un nuage de vapeur touche la vitre.",
            "narrateur|Sur le verre, un éclat de caisse cligne.",
            "narrateur|Il vient du hall, si près.",
            "narrateur|Nina ne sait pas à quoi il servira.",
            "narrateur|Papa essuie la table.",
            "narrateur|La nappe sent le thé chaud.",
            "narrateur|Une tasse fume près du torchon.",
            "narrateur|Maman plie le torchon, sans se presser.",
            "narrateur|Le tiroir fait un petit clic.",
            "papa|Nina, tu sens la pomme ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Je veux une pomme, maintenant !",
            "maman|On y va, avec le sac.",
            "narrateur|En ce moment, Nina saisit le sac bleu.",
            "narrateur|Le tissu sent le coton, un peu rêche.",
            "papa|Prends de l'eau, le hall est long.",
            "narrateur|Nina prend la gourde froide.",
            "narrateur|Le bouchon est lisse sous le doigt.",
            "enfant-f|Je mets tout, d'un coup !",
            "narrateur|Elle pousse la gourde, trop vite.",
            "narrateur|Une cuillère en bois attend près du bol.",
            "narrateur|Nina la jette dans le sac.",
            "narrateur|La cuillère fait un bruit dur.",
            "papa|La cuillère reste à la cuisine.",
            "maman|Le hall n'en a pas besoin.",
            "narrateur|Nina veut fermer, sans attendre.",
            "enfant-f|Où est mon chapeau ?",
            "narrateur|Le chapeau jaune n'est pas là.",
            "narrateur|Nina bourre le sac, quand même.",
            "narrateur|Le zip mord la sangle.",
            "enfant-f|Ça reste coincé !",
            "narrateur|Elle tire plus fort.",
            "narrateur|Le zip refuse.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu regardes le sac ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina prépare le sac.",
            "narrateur|Où met-elle les affaires ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "zip,sac",
        [
            "narrateur|Nina refuse de tirer plus fort.",
            "narrateur|Elle pose un genou au sol.",
            "narrateur|La sangle est plate, sous le zip.",
            "enfant-f|Je la sors.",
            "narrateur|Elle pousse le tissu, un peu.",
            "narrateur|Le zip lâche, petit à petit.",
            "enfant-f|Il part.",
            "papa|Sors la cuillère, d'abord.",
            "narrateur|Nina retire la cuillère en bois.",
            "narrateur|Elle la pose près de la tasse.",
            "maman|Le chapeau, sous la chaise ?",
            "narrateur|Nina se penche.",
            "narrateur|Le chapeau est souple, un peu poussiéreux.",
            "narrateur|Elle le secoue, au-dessus du sol.",
            "narrateur|Le chapeau glisse dans le sac.",
            "papa|Ton doudou voudra la pomme, lui aussi.",
            "enfant-f|Où est-il ?",
            "narrateur|Le doudou n'est pas près des chaussures.",
            "maman|Regarde sur la chaise, près du torchon.",
            "narrateur|Nina cherche près du torchon.",
            "narrateur|Le doudou sent le coton chaud.",
            "enfant-f|Il était caché.",
            "narrateur|Elle le glisse dans le sac.",
            "narrateur|La gourde reste au fond, froide.",
            "narrateur|Le zip avance, sans mordre.",
            "maman|Tu fermes, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina appuie sur la fermeture.",
            "narrateur|Ça fait un petit zzz.",
            "narrateur|Le sac bleu est fermé.",
            "papa|Merci, Nina.",
            "papa|Le sac est prêt ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina pose la main sur le tissu.",
            "narrateur|Le tissu est un peu rêche.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "hall,caisses,pas",
        [
            "papa|On met tes chaussures ?",
            "narrateur|Nina enfile ses chaussures.",
            "narrateur|Une semelle est froide.",
            "maman|Tu as fini tes chaussures ?",
            "enfant-f|Oui, maman.",
            "papa|On ouvre la porte.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air sent les caisses et le fruit.",
            "narrateur|Le hall n'est plus flou.",
            "enfant-f|Il est vrai !",
            "papa|Oui, on y va ensemble.",
            "narrateur|Nina enfile le sac.",
            "narrateur|Le sac tape contre son dos.",
            "narrateur|Ils marchent vers le hall aux caisses.",
            "narrateur|Le pavé est un peu poudreux.",
            "enfant-f|Je la prends !",
            "narrateur|Une pomme rouge brille, trop près.",
            "narrateur|Nina tend la main, trop vite.",
            "narrateur|La pomme glisse, roule sous une caisse.",
            "enfant-f|Oh.",
            "narrateur|Elle veut foncer, à quatre pattes.",
            "narrateur|Nina refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Sur le bois, un éclat de caisse cligne.",
            "narrateur|C'est celui de la vitre.",
            "enfant-f|Comme à la cuisine !",
            "maman|Tu le vois, toi ?",
            "enfant-f|Oui, sur cette caisse.",
            "narrateur|Nina s'accroupit, lente.",
            "narrateur|Elle écoute le hall, un instant.",
            "narrateur|Une autre caisse râpe, plus loin.",
            "narrateur|La pomme attend sous le bois.",
            "narrateur|Nina glisse la main, lente.",
            "narrateur|Ses doigts trouvent la peau lisse.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pomme,caisse",
        [
            "narrateur|Nina ferme la main autour de la pomme.",
            "narrateur|Le fruit reste rond, un peu froid.",
            "enfant-f|Elle brille, maman.",
            "maman|Tu la choisis ?",
            "enfant-f|Celle-là.",
            "papa|On la sent ensemble ?",
            "enfant-f|Oui.",
            "narrateur|Nina approche la pomme de son nez.",
            "narrateur|Ça sent le sucre et la peau.",
            "narrateur|Sur le bois, l'éclat de caisse reste.",
            "enfant-f|Comme sur la vitre, papa.",
            "papa|Tu le portes, toi ?",
            "enfant-f|Oui, dans mon sac.",
            "narrateur|Nina ouvre le sac, un peu.",
            "narrateur|Elle glisse la pomme contre le doudou.",
            "narrateur|Le sac repose contre sa hanche.",
            "enfant-f|On la sent, papa.",
            "maman|Tu la sens sur tes joues ?",
            "enfant-f|Oui, elle est froide.",
            "narrateur|L'éclat de caisse laisse une trace claire, sur la peau.",
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
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if blob.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{blob.count('merci')}")
    if "éclat de caisse" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de caisse" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in chunks
    )
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.001 — préparer le sac (vécue, jamais dite)\n"
        "- **Personnages :** Nina, papa, maman. Troupe D16.\n"
        "- **Lieu :** cuisine puis hall du marché (hall aux caisses)\n"
        "- **Indice unique :** éclat de caisse (vitre floue → bois de la caisse "
        "→ trace claire sur la peau)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Derrière la vitre floue, les caisses râpent le pavé. Un éclat de "
        "caisse cligne sur le verre. Nina veut une pomme du hall **maintenant**, "
        "dans son sac. Elle met tout d'un coup : gourde, cuillère en bois. Le "
        "chapeau manque. Le zip mord. Première idée ratée. Elle refuse de "
        "forcer, sort la cuillère, trouve le chapeau sous la chaise, glisse "
        "le doudou. Merci vécu. Au hall, elle tend trop vite : la pomme roule "
        "sous une caisse. Elle refuse de foncer, retrouve l'éclat de la vitre. "
        "La pomme paie le début : l'éclat laisse une trace claire sur la peau.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine, bouilloire, vapeur, vitre floue, hall qui râpe.\n"
        "- Désir : une pomme du hall, maintenant, dans le sac.\n"
        "- Objet : sac bleu, gourde, chapeau jaune, doudou. Pas la cuillère.\n"
        "- Indice unique : éclat de caisse, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : la pomme du hall, tout de suite.\n"
        "- Imprévu 1 : tout d'un coup, cuillère, chapeau absent, zip qui mord.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, après "
        "le sac fermé.\n"
        "- Imprévu 2 (plus rusé) : la pomme roule sous une caisse ; Nina veut "
        "foncer à quatre pattes.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, glisse la main.\n"
        "- Retour : pomme contre le doudou, éclat en trace claire sur la peau.\n\n"
        "## Vécu\n\n"
        "Nina veut la pomme **maintenant**. Impatience, puis sourire qui "
        "disparaît quand le zip résiste. Papa se baisse, pose une question, "
        "ne récite pas la règle. Nina agit : genou au sol, cuillère dehors, "
        "chapeau, doudou, sac. Merci vécu après la fermeture. Au hall, elle "
        "refuse de foncer. Fin : l'éclat du début est sur la peau de la pomme.\n"
        "Une pomme, pas deux. Pas de pull bleu. Pas de grain de pépin, pas de "
        "grain de pomme.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : cuisine puis hall du marché. "
        "≠ TREE-DIF-002 (pull bleu, deux pommes, grain de pépin). "
        "≠ four, ≠ cour, ≠ pente, ≠ bateau.\n"
        "- Ouverture inventée (caisses derrière la vitre floue), pas un "
        "gabarit v2, pas « Nina est dans la cuisine ».\n"
        "- Indice unique : éclat de caisse. Pas grain de miette/foin/feuille/"
        "paille/toile/pépin/pomme, pas éclat de pince/thermos/coquille/"
        "bouton/ticket/goutte/boucle/corde, pas trait de craie, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : elle prépare, porte, ose. Pas de morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (le sac). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu. Action plus vive à l'ouverture.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
