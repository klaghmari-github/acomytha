#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-07 — La plume d'Aniss (F-NAR-019, N2, AUT.AFF.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-07"
TITLE = "La plume d'Aniss"
N2 = LIMITS["N2"]
CHARS = "Aniss, papa"
SETTING = "maison au bord du bois puis chemin sous l'arbre"
FIL = (
    "Une ombre d'arbre entre dans la cuisine. Sur la vitre, un grain de pin "
    "colle. Aniss veut la plume grise sous l'arbre, maintenant, dans sa boîte. "
    "Il pousse tout dans le sac : le zip mord le chapeau. Il refuse de forcer, "
    "range une chose puis l'autre, glisse le grain. Sur le chemin, une branche "
    "barre le pas. Il refuse de foncer. Sous l'arbre, le grain de pin brille "
    "sur la plume."
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
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de pin",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_plume_maintenant; "
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
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="sac",
        note=(
            "arc=confirmation; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=une_chose_puis_la_suivante; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="grain de pin",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; sous_texte=il_refuse_de_foncer_sous_la_branche; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de pin",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_grain_de_la_vitre_est_sur_la_plume; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "le sac",
    "accepted_examples": "le sac | dans le sac | il met | elle met | mettre",
    "retry_prompt": "Il met les affaires dans le sac. Où les met Aniss ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pin,vitre,sac",
        [
            "narrateur|Une ombre d'arbre entre dans la cuisine.",
            "narrateur|Elle glisse sur la nappe, puis la tasse.",
            "narrateur|Aniss lève les yeux vers la fenêtre.",
            "narrateur|Les planches sentent la résine, tiède.",
            "narrateur|Pourtant, un détail paraît nouveau.",
            "narrateur|Une pomme de pin s'est ouverte sur le rebord.",
            "narrateur|Un grain de pin colle à la vitre.",
            "narrateur|Il est brun, collant, et il sent le bois.",
            "enfant-m|Il est tout petit, papa.",
            "papa|C'est un grain tombé du pin.",
            "narrateur|Le grain brille comme un bout d'étoile.",
            "narrateur|Dehors, le grand arbre penche vers le chemin.",
            "narrateur|Une plume grise tremble dans l'herbe, au loin.",
            "enfant-m|Je veux cette plume, maintenant !",
            "papa|Aniss, tu vois l'arbre ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Elle m'attend.",
            "papa|On y va, avec le sac.",
            "narrateur|En ce moment, Aniss saisit le sac bleu.",
            "narrateur|Le tissu gratte sous ses doigts.",
            "papa|Prends de l'eau, pour le chemin.",
            "narrateur|Aniss prend la gourde fraîche.",
            "narrateur|Le bouchon est froid sous le doigt.",
            "papa|Le chapeau aussi, les branches piquent.",
            "narrateur|Aniss prend le chapeau souple.",
            "narrateur|Le bord plie un peu, dans sa main.",
            "enfant-m|Et ma boîte à plumes ?",
            "narrateur|La boîte de bois attend sur le banc.",
            "enfant-m|Je mets tout, d'un coup !",
            "narrateur|Il pousse gourde, chapeau et boîte.",
            "narrateur|La boîte tape le fond, trop vite.",
            "narrateur|Le zip mord le bord du chapeau.",
            "enfant-m|Ça reste coincé !",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Tu regardes le zip ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss prépare le sac.",
            "narrateur|Où met-il les affaires ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "zip,tissu",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Aniss refuse de tirer plus fort.",
            "enfant-m|Je sors le chapeau.",
            "narrateur|Il tire le tissu coincé, sans forcer.",
            "narrateur|Le zip lâche, petit à petit.",
            "narrateur|Il pose le chapeau à plat, sur la table.",
            "papa|L'eau va au fond.",
            "narrateur|Aniss range la gourde froide.",
            "narrateur|La boîte de bois glisse à côté.",
            "enfant-m|Et mon doudou ?",
            "narrateur|Le doudou n'est pas près des chaussures.",
            "papa|Regarde le banc sous la fenêtre.",
            "narrateur|Aniss cherche près du banc.",
            "narrateur|Le doudou sent le coton, un peu chaud.",
            "enfant-m|Te voilà.",
            "narrateur|Il le glisse dans le sac.",
            "papa|Merci, Aniss.",
            "narrateur|Le zip avance, sans mordre.",
            "enfant-m|Il part.",
            "papa|Le sac est prêt ?",
            "enfant-m|Pas le grain.",
            "papa|Tu prends aussi le grain de pin ?",
            "enfant-m|Oui, pour la plume.",
            "narrateur|Aniss détache le grain de la vitre.",
            "narrateur|Il le pose dans la boîte de bois.",
            "narrateur|Aniss appuie sur la fermeture.",
            "narrateur|Ça fait un petit zzz.",
            "narrateur|Le sac bleu est fermé.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "chemin,branches",
        [
            "papa|On met tes chaussures ?",
            "narrateur|Aniss enfile ses chaussures.",
            "narrateur|Une semelle est froide, contre le sol.",
            "papa|Tu as fini tes chaussures ?",
            "enfant-m|Oui, papa.",
            "papa|On ouvre la porte.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air sent la résine et l'herbe sèche.",
            "narrateur|Le sac bleu tape contre sa hanche.",
            "enfant-m|On va voir la plume ?",
            "papa|Oui, sous le grand arbre.",
            "narrateur|Ils marchent sur le chemin du bois.",
            "narrateur|Les aiguilles de pin craquent sous les pas.",
            "enfant-m|Je la vois, papa !",
            "narrateur|Une plume grise brille, plus loin.",
            "enfant-m|Je cours la prendre !",
            "narrateur|Aniss veut partir sans le sac.",
            "narrateur|Une branche basse barre le pas.",
            "narrateur|Le sourire d'Aniss se serre.",
            "narrateur|Ça serre, dans son ventre.",
            "enfant-m|Je n'aime pas ça.",
            "narrateur|Aniss refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Aniss observe le sac, écoute le bois.",
            "narrateur|Dans la boîte, le grain de pin a bougé.",
            "narrateur|Il penche vers la branche basse.",
            "enfant-m|C'est par là.",
            "papa|Tu contournes, ou tu pousses ?",
            "enfant-m|Je contourne.",
            "narrateur|Il recule d'un pas.",
            "narrateur|Il passe sous la branche, lentement.",
            "narrateur|Le sac reste bien fermé.",
            "enfant-m|Elle est là.",
            "papa|Oui, dans l'herbe.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "arbre,plume",
        [
            "narrateur|Ils s'arrêtent sous le grand arbre.",
            "narrateur|L'ombre de l'arbre touche les joues d'Aniss.",
            "enfant-m|La plume est là.",
            "papa|Oui, elle t'attendait.",
            "narrateur|Une plume grise repose dans l'herbe sèche.",
            "narrateur|Sur la plume, un grain de pin brille.",
            "enfant-m|Comme sur la vitre, papa !",
            "papa|Tu la prends, toi ?",
            "enfant-m|Oui, dans ma boîte.",
            "narrateur|Aniss ouvre le sac, sans se presser.",
            "narrateur|Il glisse la plume contre le grain de pin.",
            "narrateur|Le grain colle un peu à la plume.",
            "enfant-m|Ils voyagent ensemble.",
            "papa|Tu les sens, sur tes doigts ?",
            "enfant-m|Oui, ça sent le bois.",
            "narrateur|Le sac repose contre sa hanche.",
            "narrateur|Le grain de pin brille sur la plume.",
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
        extra_kw: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra_kw["pause_before_ms"] = 200
            extra_kw["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra_kw["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra_kw)
    merged = dict(src)
    merged["fil_rouge"] = FIL
    merged["title"] = TITLE
    merged["characters"] = CHARS
    merged["setting"] = SETTING
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    blob = "\n".join(c["script"] for c in merged["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    opening = by["CHK_T0000_P0000"]["text"].lower()
    ending = by["CHK_T0000_P0000_END_F0001"]["text"].lower()
    if "grain de pin" not in opening:
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "grain de pin" not in ending:
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
        "Une ombre d'arbre entre dans la cuisine. Une pomme de pin s'ouvre "
        "sur le rebord. Un grain de pin colle à la vitre. Aniss veut la plume "
        "grise sous le grand arbre, **maintenant**, dans sa boîte. Il pousse "
        "gourde, chapeau et boîte d'un coup : le zip mord le chapeau. Première "
        "idée ratée. Papa s'accroupit. Aniss refuse de forcer, range une chose "
        "puis l'autre, glisse le doudou, détache le grain. Merci vécu. Sur le "
        "chemin, il veut courir sans le sac : une branche barre le pas. Il "
        "refuse de foncer. Le grain penche vers la branche. Il contourne. "
        "Sous l'arbre, le grain de pin brille sur la plume. Il les glisse "
        "ensemble dans la boîte.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison au bord du bois, ombre d'arbre sur la nappe, résine, "
        "rebord, vitre, grand arbre au loin.\n"
        "- Désir : porter la plume grise dans la boîte, maintenant.\n"
        "- Objet : sac bleu, gourde, chapeau, boîte de bois, doudou, plume.\n"
        "- Indice unique : grain de pin, vu dès l'ouverture, payé sous l'arbre.\n"
        "- Urgence douce : la plume tremble dans l'herbe, au loin.\n"
        "- Imprévu 1 : tout d'un coup, zip qui mord, chapeau coincé.\n"
        "- Cue : papa à la même hauteur, une chose puis la suivante. "
        "Un merci vécu, après le doudou rangé.\n"
        "- Imprévu 2 (plus rusé) : il veut courir sans le sac ; une branche "
        "basse barre le pas.\n"
        "- Résolution : il refuse de foncer, lit le grain dans la boîte, "
        "contourne, sac fermé.\n"
        "- Retour : sous l'arbre, le grain de la vitre brille sur la plume.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.001 (préparer le sac) greffée, jamais dite. La première "
        "idée (tout d'un coup) échoue. Le choix d'Aniss change l'action. "
        "Un « en ce moment ». Un merci vécu. Adulte + question. Troupe D16 : "
        "Aniss, papa.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : maison au bord du bois puis chemin "
        "sous l'arbre. ≠ four, ≠ cour, ≠ pente, ≠ jardin/escargot.\n"
        "- Ouverture inventée (ombre d'arbre sur la nappe), pas un gabarit v2.\n"
        "- Indice unique : grain de pin. Pas grain de miette/foin/feuille/"
        "paille/toile/pépin/pomme/carotte, pas éclat de pince/thermos/"
        "coquille/bouton/ticket/goutte/boucle/corde/caisse, pas trait de "
        "craie, merle, miel.\n"
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
