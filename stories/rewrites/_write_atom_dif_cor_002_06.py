#!/usr/bin/env python3
"""ATOM-DIF.COR.002-06 — Les lanternes de Chouchou (F-NAR-019, N2, DIF.COR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.002-06"
TITLE = "Les lanternes de Chouchou"
N2 = LIMITS["N2"]
CHARS = "Chouchou, Mila, papa, maman"
SETTING = (
    "perron au crépuscule, pots de confiture, sucre, papier jaune, "
    "pierre tiède, fenêtre jaune"
)
INDICE = "éclat de perron"
FIL = (
    "Un reste de sucre capte le dernier soleil, au fond des pots. "
    "Sur la pierre, un éclat de perron brille. Chouchou veut des "
    "lanternes maintenant. Elle pousse trop vite : le papier se "
    "froisse, le couvercle résiste, l'éclat glisse. Mila prend son "
    "temps. Un petit rire commence, puis s'arrête. Elle refuse de "
    "foncer, propose. Mila regarde. Merci vécu. Lever trop vite : "
    "le papier file. Elle refuse, retrouve l'éclat. L'éclat de "
    "perron tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(chaise|tiroir|fraisier|cuivre|buis|biscuit|biscuits|"
    r"citron|casserole|guirlande|fraise|fraises|tarte|drap|draps|"
    r"cheval|haie|abeille|argile|écurie|ecurie|carton|ballon|"
    r"limace|tablier|zeste|zestes|escargot|arrosoir|ciseaux|"
    r"pince|cabane|tunnel|coquille|beurre|farine)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "c'est la règle",
    "bon travail",
    "tu as bien fait",
    "tu as su",
    "l'amitié ne dépend",
    "l'amitie ne depend",
    "corps plus rond",
    "corps plus mince",
    "formes différentes",
    "formes differentes",
    "n'a pas la même forme",
    "n'a pas la meme forme",
    "pas une blague",
    "n'est pas une blague",
    "n est pas une blague",
    "vous jouez",
    "on joue",
    "on cuisine",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de tiroir",
    "éclat de chaise",
    "éclat de fraisier",
    "éclat de pierre",
    "éclat de pot",
    "éclat de sucre",
    "éclat de verre",
    "éclat de papier",
    "éclat de lanterne",
    "éclat de marche",
    "éclat de fenêtre",
    "éclat de fenetre",
    "éclat de carton",
    "éclat de couloir",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de sac",
    "éclat de poire",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de planche",
    "éclat de robinet",
    "éclat de figue",
    "éclat de coussin",
    "éclat de samare",
    "éclat de bassine",
    "éclat d'émail",
    "éclat d'email",
    "éclat de cerceau",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "grain de",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de perron",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_les_lanternes_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="blague",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_rire_s_est_arrete_elles_peuvent_jouer; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="papier",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_propose_mila_regarde_elles_glissent_le_papier; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de perron",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_lever_trop_vite; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de perron",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_pierre; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": (
        "jouer | on joue | pas une blague | pas blague | les lanternes"
    ),
    "retry_prompt": "On joue. Que fait Chouchou ?",
    "engine_ok_text": "Oui, on joue.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

P0000 = [
    "narrateur|Un reste de sucre capte le dernier soleil.",
    "narrateur|Il brille au fond d'un pot de confiture.",
    "enfant-f|Ça brille, papa !",
    "papa|Tu le vois, dans le verre ?",
    "enfant-f|Oui, un petit point.",
    "narrateur|Deux pots vides attendent au bord du perron.",
    "narrateur|Le verre est lisse, un peu froid.",
    "maman|Le perron est tiède, sous tes pieds ?",
    "enfant-f|Oui, maman.",
    "enfant-f|La pierre est chaude.",
    "narrateur|Sur la pierre, un éclat de perron brille.",
    "enfant-f|Il brille aussi.",
    "papa|C'est le soleil, sur la pierre ?",
    "enfant-f|Oui, tout petit.",
    "narrateur|Le ciel devient violet, au-dessus du toit.",
    "narrateur|Ça sent l'herbe coupée, près des marches.",
    "enfant-f|Ça sent le sucre aussi.",
    "maman|Un peu, oui.",
    "narrateur|Un papillon de nuit tourne près de la fenêtre.",
    "narrateur|La fenêtre de la cuisine est jaune.",
    "enfant-f|Je veux des lanternes, maintenant !",
    "papa|Avec les pots ?",
    "enfant-f|Oui, et du papier jaune.",
    "maman|On les lève vers le ciel ?",
    "enfant-f|Oui, maman !",
    "narrateur|Papa tend deux papiers jaunes.",
    "narrateur|Ils froissent, fins, entre les doigts.",
    "enfant-f|Il fait un bruit de papier.",
    "narrateur|En ce moment, Chouchou pousse le papier trop vite.",
    "narrateur|Le papier se froisse au fond du pot.",
    "narrateur|Le sucre colle au jaune.",
    "enfant-f|Oh.",
    "narrateur|Le couvercle reste coincé.",
    "enfant-f|Il ne veut pas !",
    "narrateur|Mila arrive sur la première marche.",
    "narrateur|Ses chaussons font un bruit mou.",
    "narrateur|Elle prend son temps, un pied, puis l'autre.",
    "enfant-f|Mila !",
    "copine|J'arrive.",
    "maman|Tes chaussons sont mous, Mila ?",
    "copine|Oui.",
    "enfant-f|Les lanternes, maintenant, Mila !",
    "narrateur|Chouchou tire le pot trop vite vers Mila.",
    "copine|Non.",
    "narrateur|Mila recule d'une marche.",
    "enfant-f|Oh.",
    "narrateur|Un petit rire commence, chez Chouchou.",
    "narrateur|Mila baisse les yeux.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Le rire s'arrête net.",
    "narrateur|Chouchou ferme la bouche.",
    "narrateur|Ses joues sont chaudes, un peu.",
    "narrateur|L'éclat de perron glisse sur la pierre.",
    "enfant-f|Il part.",
    "narrateur|Le sourire de Chouchou disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|Tu parles à Mila, Chouchou ?",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "enfant-f|Oui, papa.",
    "maman|Tes mains tiennent le verre ?",
    "enfant-f|Oui, maman.",
    "narrateur|Les mots se perdent près des pots.",
    "narrateur|Personne n'entend la fin.",
    "narrateur|Le papier reste froissé, au fond.",
]

Q0001 = [
    "narrateur|Le corps n'est pas une blague.",
    "narrateur|Que fait-on ?",
]

C0001 = [
    "narrateur|Chouchou avance le pot trop vite.",
    "enfant-f|Tu pousses le papier, maintenant !",
    "narrateur|Les mots se bousculent dans sa bouche.",
    "copine|Non.",
    "narrateur|Mila reste sur la marche.",
    "enfant-f|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Chouchou refuse de foncer.",
    "narrateur|Elle recule le pot, un peu.",
    "papa|Le papier est froissé, Chouchou ?",
    "narrateur|Papa reste à sa hauteur.",
    "maman|Le sucre colle, sous tes doigts.",
    "narrateur|Maman n'a pas fini non plus.",
    "narrateur|Chouchou attend que le silence arrive.",
    "enfant-f|Tu veux tourner le couvercle ?",
    "narrateur|Mila ne dit rien.",
    "narrateur|Elle s'assoit sur la marche.",
    "copine|Je regarde.",
    "enfant-f|D'accord.",
    "papa|Merci, Chouchou.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu tiens le verre des deux mains ?",
    "enfant-f|Oui, maman.",
    "enfant-f|Il est froid.",
    "papa|Tu parles du sucre, si tu veux ?",
    "enfant-f|Le sucre capte le soleil.",
    "maman|On reste au perron, Chouchou ?",
    "enfant-f|Oui.",
    "narrateur|Chouchou glisse le papier sans presser.",
    "narrateur|Le jaune se pose contre le verre.",
    "narrateur|Mila tourne le couvercle, sans se presser.",
    "narrateur|Le couvercle vient, sans un à-coup.",
    "enfant-f|Il est ouvert.",
    "copine|Le mien aussi.",
    "papa|Tu as entendu le verre ?",
    "enfant-f|Oui, papa.",
    "narrateur|Elles lèvent un peu les pots.",
    "narrateur|Le dernier soleil traverse le jaune.",
    "enfant-f|Ça brille.",
    "copine|La mienne aussi.",
    "narrateur|Le ventre de Chouchou se desserre.",
]

END = [
    "narrateur|Chouchou veut lever les pots, d'un coup.",
    "enfant-f|On les lève, maintenant !",
    "narrateur|Elle lève trop vite.",
    "narrateur|Le papier glisse vers le bord.",
    "enfant-f|Oh.",
    "narrateur|Papa n'a pas fini sa phrase.",
    "papa|Le papier file, Chouchou.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-f|Oh.",
    "narrateur|Chouchou refuse de foncer, cette fois.",
    "narrateur|Ses mains se ferment, puis s'ouvrent.",
    "narrateur|Elle écoute le perron, un instant.",
    "narrateur|Elle observe le pot, écoute la pierre.",
    "narrateur|Sur la pierre, un éclat de perron luit.",
    "enfant-f|Il est là.",
    "enfant-f|Tu lèves le tien, si tu veux ?",
    "copine|Plus tard.",
    "enfant-f|D'accord.",
    "narrateur|Mila reste à regarder.",
    "narrateur|Chouchou lève le pot sans presser.",
    "narrateur|Le jaune s'allume dans le verre.",
    "enfant-f|C'est une lanterne.",
    "papa|Tu restes un peu ?",
    "enfant-f|Oui, papa.",
    "maman|Les pots sont près de la marche.",
    "enfant-f|On les pose ?",
    "papa|Oui, sur la pierre.",
    "narrateur|Le verre sent le sucre.",
    "enfant-f|Il colle aux doigts.",
    "maman|Comme le reste, oui.",
    "narrateur|Mila lève le sien, sans un mot.",
    "narrateur|Le jaune s'allume aussi, chez elle.",
    "copine|La mienne brille.",
    "enfant-f|Les deux brillent.",
]

FIN = [
    "narrateur|Elles restent près des pots.",
    "narrateur|Maman pose les deux verres côte à côte.",
    "enfant-f|Comme deux lunes, papa.",
    "papa|Tu les vois, toi ?",
    "enfant-f|Oui, sur la pierre.",
    "maman|On est bien, ici.",
    "narrateur|Chouchou glisse le doigt, sans se presser.",
    "enfant-f|On le sent, maman.",
    "maman|Tu le sens sur tes doigts ?",
    "enfant-f|Oui, il colle.",
    "papa|Les lanternes sont posées, Chouchou.",
    "enfant-f|Oui, avec Mila.",
    "narrateur|L'odeur d'herbe reste sur le perron.",
    "enfant-f|Il est là, maman.",
    "maman|Oui, sur la pierre.",
    "narrateur|Le ciel est presque bleu nuit.",
    "copine|Deux petites.",
    "narrateur|Un peu de sucre tient au verre.",
    "narrateur|L'éclat de perron tient sur la pierre.",
]


def vet(lines: list[str], *, allow_lesson: bool = False) -> list[str]:
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not allow_lesson:
            for bad in EXTRA_BAD:
                if bad in low:
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copine"):
            raise SystemExit(f"rôle {role}: {raw}")
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
    lines = vet(lines, allow_lesson=bool(extra.get("allow_lesson")))
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
    out["pitch_xai_tag"] = m.get("pitchTag")
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
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    wanted = {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in wanted]
    extra = wanted - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "sucre,pots,papier",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "allow_lesson": True,
                "fields": Q_FIELDS,
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "verre,couvercle",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "papier,pierre",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "perron",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    for c in src["chunks"]:
        if c.get("kind") != by[c["chunk_id"]].get("kind"):
            raise SystemExit(f"{c['chunk_id']}: kind changé")
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Chouchou = enfant-f)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Mila absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copine") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copine" for r in roles):
        raise SystemExit(f"{SID}: copine absente")
    recit = "\n".join(
        c["script"]
        for c in chunks
        if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for slogan in (
        "pas une blague",
        "corps n'est pas",
        "corps n est pas",
        "on joue",
        "vous jouez",
        "corps plus rond",
        "corps plus mince",
        "l'amitié ne dépend",
        "chaise",
        "tiroir",
        "fraisier",
        "cuivre",
        "buis",
    ):
        if slogan in recit:
            raise SystemExit(f"{SID}: récitation {slogan!r}")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le corps n'est pas une blague. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "")
    if "mila" in retry.lower():
        raise SystemExit(f"{SID}: retry 2e enfant")
    if "chouchou" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Chouchou")
    if "jouer" not in retry.lower() and "joue" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans jouer")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "non" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans non")
    if "regarde" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans je regarde")
    if "plus tard" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans plus tard")
    if "d'accord" not in recit:
        raise SystemExit(f"{SID}: Chouchou n'accepte pas")
    for ban in (
        "éclat de cuivre",
        "éclat de buis",
        "éclat de tiroir",
        "éclat de chaise",
        "éclat de fraisier",
        "éclat de pierre",
        "lise",
        "kilian",
        "flamme",
        "bougie",
        "allumette",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and str(c["text_ssml"]).startswith("<speak>")
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
        "- **Public :** N2 (≤15 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.002 — le corps n'est pas une blague / on "
        "joue (vécue : Mila prend son temps sur la marche ; un petit rire "
        "commence ; elle baisse les yeux ; Chouchou ferme la bouche ; "
        "elles glissent le papier, ensemble. Jamais dite dans le récit.)\n"
        "- **Personnages :** Chouchou, Mila, papa, maman. Troupe D16. "
        "Dump `enfant-m` → `enfant-f` (Chouchou). Mila = `copine`. "
        "Maman ajoutée (dump : papa seulement). Adultes parlants = "
        "papa/maman.\n"
        "- **Lieu :** perron au crépuscule, pots de confiture, sucre, "
        "papier jaune, pierre tiède, fenêtre jaune. ≠ 002-01 cuisine / "
        "cuivre / biscuits. ≠ 002-02 chemin / buis / cheval. ≠ 002-03 "
        "salle / tiroir / guirlande. ≠ 002-04 fraisiers. ≠ 002-05 salon "
        "/ chaise / draps.\n"
        "- **Indice unique :** éclat de perron (brille à l'ouverture → "
        "glisse quand elle fonce → luit au refus → tient sur la pierre). "
        "Pas éclat de cuivre / buis / tiroir / chaise / fraisier.\n"
        "- **Question moteur :** « Le corps n'est pas une blague. Que "
        "fait-on ? » expected **jouer**. retry : Que fait Chouchou ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un reste de sucre capte le dernier soleil, au fond d'un pot. "
        "Sur la pierre, un éclat de perron brille. Chouchou veut des "
        "lanternes **maintenant**. Elle pousse trop vite : le papier se "
        "froisse, le sucre colle, le couvercle résiste. Mila arrive, un "
        "pied puis l'autre. Chouchou tire le pot : non. Un petit rire "
        "commence. Mila baisse les yeux. Le rire s'arrête. L'éclat "
        "glisse. Sourire parti. Papa s'accroupit. Elle refuse de foncer, "
        "propose. Mila regarde. Merci vécu. Papier glissé, couvercle à "
        "deux. Deuxième ruse : lever maintenant ; le papier file. Elle "
        "refuse, retrouve l'éclat. Plus tard. Deux lunes. L'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : perron au crépuscule, pots de confiture, sucre, "
        "pierre tiède, herbe coupée, papillon de nuit, fenêtre jaune. "
        "≠ 002-01..05.\n"
        "- Désir : des lanternes de papier jaune dans les pots, levées "
        "vers le ciel, maintenant.\n"
        "- Objet : pots, sucre, papier jaune, couvercle, pierre.\n"
        "- Indice unique : éclat de perron, vu dès l'ouverture, payé "
        "sur la pierre au retour.\n"
        "- Urgence douce : le dernier soleil, les pots vides, Mila "
        "sur la marche.\n"
        "- Imprévu 1 : papier trop vite, couvercle coincé, pot tiré, "
        "non, petit rire qui s'arrête, éclat qui glisse.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord » près de la marche.\n"
        "- Imprévu 2 (plus rusé) : lever les pots maintenant ; le "
        "papier file, les voix se mélangent.\n"
        "- Résolution : elle refuse de foncer, propose, accepte le "
        "silence, le regard, plus tard. Elles jouent : papier, "
        "couvercle, soleil dans le jaune.\n"
        "- Retour : deux pots côte à côte (deux lunes), sucre au "
        "verre, l'éclat tient sur la pierre.\n\n"
        "## Vécu\n\n"
        "Leçon DIF.COR.002 greffée, jamais annoncée. Chouchou veut "
        "les lanternes **maintenant**. Impatience, puis joues chaudes "
        "quand le rire s'arrête. Mila prend son temps ou pose sa "
        "limite. Le silence compte. La première idée (tirer, foncer) "
        "échoue. Le choix de Chouchou change l'action : elles jouent. "
        "Un « en ce moment ». Un merci vécu. Adulte + question. Troupe "
        "D16 : Chouchou, Mila, papa, maman. N2.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Les lanternes de Chouchou (noyau dump).\n"
        "- Héros Chouchou, fille. Dump `enfant-m` → `enfant-f`. Mila "
        "conservée, `copine`. Deux rythmes, sans voix caricaturale.\n"
        "- Maman ajoutée (dump : papa seulement).\n"
        "- Question moteur : « Le corps n'est pas une blague. Que "
        "fait-on ? » Fond **jouer** conservé. retry Lise absent, "
        "Chouchou nommé. Pas de récitation dans le récit.\n"
        "- Ouverture inventée (un reste de sucre capte le dernier "
        "soleil), pas un gabarit v2, pas « joue au salon ».\n"
        "- Indice unique : éclat de perron. Pas chaise / tiroir / "
        "fraisier / cuivre / buis. Pas de flamme (soleil dans le "
        "papier).\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Dump « tout calmes / encore » jeté.\n"
        "- Leçon non dite : pas « on joue » dans le récit, pas "
        "« corps plus rond / plus mince », pas « l'amitié ne dépend "
        "pas de la forme ».\n"
        "- 5 chunks, kinds inchangés. example4 : 006, 038, 070. "
        "Voix : `_write_atom_col_pol_001_11.py` (Chouchou).\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
