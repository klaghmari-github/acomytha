#!/usr/bin/env python3
"""ATOM-DIF.COR.001-01 — Le bol de fraises (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-01"
TITLE = "Le bol de fraises"
N1 = LIMITS["N1"]
INDICE = "éclat d'émail"
FIL = (
    "L'eau glisse. Le bol émaillé est froid. Sur le bord, un éclat "
    "d'émail brille. Victorino veut des fraises, maintenant, avec Nina. "
    "Il lève trop haut : le bol penche, l'éclat saute. Il refuse de "
    "foncer, cueille bas, Nina haut. Merci vécu. Vers le plaid, il porte "
    "trop haut : ça roule. Il tient le fond, Nina le bord. L'éclat "
    "d'émail tient."
)
CHARS = "Victorino, Nina, papa, maman"
SETTING = "jardin, fraisiers, plaid sous le cerisier, bol émaillé"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "dorian",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "ninon",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai levé la main",
    "j'ai leve la main",
    "j'ai attendu",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "on range les feutres",
    "tu ranges",
    "tu as bien écouté",
    "tu as bien ecoute",
    "on aime écouter",
    "on aime ecouter",
    "écoute la maîtresse",
    "ecoute la maitresse",
    "tu as bien fait",
    "bon travail",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "tu attends ton tour",
    "c'est ton tour",
    "on doit demander",
    "il faut demander",
    "tu as attendu",
    "même leçon",
    "même règle",
    "c'est la règle",
    "jouer ensemble",
    "tailles différentes",
    "tailles differentes",
    "petit ou grand",
    "vous jouez",
    "on peut jouer",
    "on joue ensemble",
    "gouttière",
    "gouttiere",
    "crayon",
    "buée",
    "buee",
    "croûte",
    "croute",
    "tableau",
    "casier",
    "moufle",
    "craie",
    "cartable",
    "pinceau",
    "casserole",
    "enveloppe",
    "dalle",
    "plaque",
    "pierre",
    "grille",
    "couvercle",
    "cheminée",
    "cheminee",
    "grain de",
    "éclat de mie",
    "éclat de croûte",
    "éclat de croute",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de terre",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
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
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "éclat de crayon",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de craie",
    "éclat de tapis",
    "éclat de moufle",
    "éclat de casier",
    "éclat de tableau",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de grille",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de dalle",
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "éclat de samare",
    "éclat de bassine",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "malaise",
    "secret",
    "feuille collée au lait",
    "bouteille de lait",
)


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat d'émail",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_les_fraises_maintenant_avec_nina; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Nina",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_invite_nina_ils_restent_pres_des_fraisiers; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Ding",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_cueille_bas_nina_haut; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="bol",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_tient_le_fond_nina_le_bord; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat d'émail",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bol; "
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
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
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
    "narrateur|L'eau glisse sur le bord.",
    "narrateur|Elle est froide.",
    "narrateur|Le bol émaillé vient du robinet.",
    "narrateur|Maman l'a rincé.",
    "narrateur|Papa tient le torchon bleu.",
    "enfant-m|Il est froid, papa !",
    "papa|Tu as senti l'eau ?",
    "enfant-m|Oui, papa.",
    "narrateur|Le jardin sent la terre.",
    "narrateur|La terre est tiède.",
    "narrateur|Le cerisier fait de l'ombre.",
    "narrateur|Un plaid attend dessous.",
    "maman|Le plaid est prêt ?",
    "enfant-m|Oui, maman.",
    "narrateur|Sur le bord, un éclat d'émail brille.",
    "enfant-m|Il est blanc, maman.",
    "maman|Tu le vois sur le bol ?",
    "enfant-m|Oui, il brille.",
    "papa|C'est l'émail, sous la lumière.",
    "enfant-m|Je veux des fraises.",
    "enfant-m|Maintenant !",
    "maman|Pour le goûter, sur le plaid ?",
    "enfant-m|Oui.",
    "narrateur|Les fraisiers sentent le sucre.",
    "narrateur|Les feuilles sont un peu râpeuses.",
    "narrateur|Une fraise basse est chaude.",
    "enfant-m|Le soleil l'a chauffée.",
    "papa|Elle est rouge, celle-là ?",
    "enfant-m|Oui, toute rouge.",
    "narrateur|Nina arrive près du cerisier.",
    "narrateur|Ses mains touchent les hautes feuilles.",
    "enfant-m|Tu viens ?",
    "copine|Oui.",
    "narrateur|Ils posent le bol dans l'herbe.",
    "narrateur|Nina cueille une fraise haute.",
    "narrateur|Elle la laisse tomber dans le bol.",
    "narrateur|Le bol sonne un petit ding.",
    "enfant-m|Ding !",
    "narrateur|En ce moment, Victorino lève la main.",
    "narrateur|Une fraise rouge est trop haut.",
    "narrateur|Sa main n'arrive pas.",
    "enfant-m|Elle est trop haut !",
    "narrateur|Il saisit le bol trop vite.",
    "narrateur|Le bol penche vers l'herbe.",
    "narrateur|L'éclat d'émail saute près du bol.",
    "enfant-m|Oh.",
    "narrateur|Le sourire de Victorino disparaît.",
    "narrateur|Dans sa poitrine, ça se bouscule.",
    "narrateur|L'envie et l'inquiétude se heurtent.",
    "enfant-m|Ça ne veut pas !",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tes doigts sont près du bol ?",
    "enfant-m|Oui, papa.",
    "maman|On essuie tes genoux.",
    "maman|Voilà.",
    "enfant-m|C'est tiède.",
    "papa|C'est la terre, Victorino.",
    "narrateur|Une feuille colle au poignet.",
    "narrateur|Victorino la retire.",
    "narrateur|Nina reste près des hautes feuilles.",
    "narrateur|Elle ne dit rien.",
    "enfant-m|La haute, Nina !",
    "narrateur|Victorino veut la haute, tout de suite.",
    "narrateur|Il tend le bras trop loin.",
]

Q0001 = [
    "narrateur|Victorino invite Nina.",
    "narrateur|Que font-ils ?",
]

C0001 = [
    "narrateur|Victorino veut la fraise haute.",
    "narrateur|Il saute un peu.",
    "narrateur|Sa main touche la feuille.",
    "narrateur|La fraise reste trop haut.",
    "enfant-m|Je l'ai !",
    "narrateur|Nina avance la main aussi.",
    "narrateur|Les deux mains se heurtent.",
    "narrateur|La fraise bascule.",
    "narrateur|Le bol tremble dans l'herbe.",
    "enfant-m|Oh.",
    "copine|Non.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Victorino refuse de foncer.",
    "narrateur|Il repose le bol.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il écoute les feuilles du jardin.",
    "narrateur|Il regarde le bol, puis Nina.",
    "narrateur|Sur le bord, l'éclat d'émail revient.",
    "enfant-m|Il est là.",
    "narrateur|Une fraise basse touche son genou.",
    "narrateur|Il la cueille près du genou.",
    "narrateur|Il la fait rouler vers le bol.",
    "narrateur|La fraise tombe dedans.",
    "narrateur|Le bol sonne.",
    "enfant-m|Ding.",
    "narrateur|Nina cueille une haute.",
    "narrateur|Elle la laisse tomber.",
    "narrateur|Le bol sonne, plus fort.",
    "copine|Ding.",
    "enfant-m|La mienne aussi.",
    "papa|Merci, Victorino.",
    "narrateur|Papa a regardé jusqu'au bout.",
    "maman|Le bol est lourd, non ?",
    "enfant-m|Oui, maman.",
    "papa|On va sous le cerisier ?",
    "enfant-m|Le goûter, oui.",
    "narrateur|Le ventre de Victorino se desserre.",
]

END = [
    "narrateur|Ils marchent vers le plaid.",
    "narrateur|L'ombre du cerisier est fraîche.",
    "narrateur|Les fraises sentent fort.",
    "enfant-m|Je le porte !",
    "narrateur|Victorino lève le bol trop haut.",
    "narrateur|Ses bras tremblent un peu.",
    "narrateur|Une fraise roule vers l'herbe.",
    "enfant-m|Ça roule !",
    "narrateur|Nina veut le reprendre, d'un coup.",
    "narrateur|Le bol penche de l'autre côté.",
    "enfant-m|Oh.",
    "narrateur|Victorino refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il regarde le bol.",
    "narrateur|Il écoute le cerisier.",
    "enfant-m|En bas, moi.",
    "narrateur|Nina ne dit rien.",
    "narrateur|Elle prend le bord, plus haut.",
    "narrateur|Victorino tient le fond.",
    "narrateur|Le bol ne penche plus.",
    "enfant-m|Il est lourd.",
    "copine|Oui.",
    "papa|Tes pieds sont dans l'herbe ?",
    "enfant-m|Oui, papa.",
    "maman|On pose le bol ?",
    "enfant-m|Sur le plaid.",
    "narrateur|Ils posent le bol sur le plaid.",
    "narrateur|Le plaid est un peu rêche.",
    "narrateur|Victorino s'assoit près du bol.",
    "narrateur|Nina s'assoit, les genoux plus hauts.",
    "enfant-m|Une basse !",
    "narrateur|Il fait rouler une fraise.",
    "narrateur|Elle tombe dans le bol.",
    "narrateur|Nina en laisse tomber une.",
    "narrateur|Le bol sonne deux fois.",
    "enfant-m|Ding ding.",
    "papa|Tu l'entends, le petit bruit ?",
    "enfant-m|Oui, papa.",
]

FIN = [
    "narrateur|Ils restent sur le plaid.",
    "narrateur|Le bol n'est plus froid.",
    "enfant-m|Comme tout à l'heure, papa !",
    "papa|Tu le vois, le petit bord ?",
    "enfant-m|Oui, l'éclat.",
    "maman|On est bien, ici.",
    "narrateur|Le cerisier sent un peu le sucre.",
    "narrateur|Victorino glisse le pied, sans se presser.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est tiède.",
    "narrateur|Une goutte de jus sèche au bord.",
    "enfant-m|L'éclat, il est là.",
    "papa|On le laisse ?",
    "enfant-m|Oui.",
    "narrateur|L'éclat d'émail tient sur le bol.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
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
        raise SystemExit(f"{SID} chunks inattendus missing={missing} extra={extra}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "jardin,bol,feuilles",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "jouer ensemble",
                    "accepted_examples": (
                        "jouer ensemble | ensemble | ils jouent | on joue | jouer"
                    ),
                    "retry_prompt": (
                        "Ils jouent. Que font Victorino et Nina ?"
                    ),
                    "engine_ok_text": "Oui, ils jouent ensemble.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "bol,fraises",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "plaid,pas",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "cerisier,bol",
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
    if "dorian" in blob:
        raise SystemExit(f"{SID}: Dorian interdit")
    if "ninon" in blob:
        raise SystemExit(f"{SID}: Ninon interdite")
    if "éclat de fraise" in blob:
        raise SystemExit(f"{SID}: BAN éclat de fraise")
    for bad in (
        "enveloppe", "dalle", "plaque", "pierre", "grille",
        "couvercle", "cheminée", "cheminee",
    ):
        if re.search(rf"\b{bad}\b", blob):
            raise SystemExit(f"{SID}: BAN {bad}")
    if "jouer ensemble" in blob:
        raise SystemExit(f"{SID}: leçon dite")
    if "tailles différentes" in blob or "tailles differentes" in blob:
        raise SystemExit(f"{SID}: leçon dite (tailles)")
    if "petit ou grand" in blob:
        raise SystemExit(f"{SID}: leçon dite (petit ou grand)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if not all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Victorino invite Nina. Que font-ils ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer ensemble":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "dorian" in retry.lower() or "ninon" in retry.lower():
        raise SystemExit(f"{SID}: retry prénom hors dump")
    if "victorino" not in retry.lower() or "nina" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans héros: {retry}")
    kinds = {c["chunk_id"]: by_src[c["chunk_id"]].get("kind") for c in src["chunks"]}
    for c in chunks:
        if c.get("kind") != kinds[c["chunk_id"]]:
            raise SystemExit(f"{SID}: kind altéré {c['chunk_id']}")

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
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.001 — jouer ensemble (grand/petit) (vécue : "
        "Victorino lève trop haut, le bol penche ; il cueille bas, Nina "
        "haut ; vers le plaid il porte trop haut, ça roule ; il tient le "
        "fond, Nina le bord). Jamais dite.\n"
        "- **Personnages :** Victorino, Nina, papa, maman. Papa ajouté. "
        "Nina = copine (rythme lent, limite). Troupe D16.\n"
        "- **Lieu :** jardin, fraisiers, plaid sous le cerisier, bol "
        "émaillé, terre tiède, torchon bleu\n"
        "- **Indice unique :** éclat d'émail (bord du matin → saute près "
        "du bol → revient sur le bord → tient à la fin). Pas éclat de "
        "fraise (BAN). Pas enveloppe, dalle, plaque, pierre, grille, "
        "couvercle, cheminée.\n"
        "- **Question moteur :** Victorino invite Nina. Que font-ils ? → "
        "jouer ensemble. retry : Que font Victorino et Nina ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "L'eau glisse sur le bord. Le bol émaillé vient du robinet. Sur le "
        "bord, un éclat d'émail brille. Victorino veut des fraises "
        "**maintenant**, avec Nina, pour le goûter sur le plaid. Il "
        "invite : « Tu viens ? ». Nina laisse tomber une haute : ding. "
        "Il lève trop haut : sa main n'arrive pas, le bol penche, "
        "l'éclat saute. Sourire parti, poitrine qui se bouscule. Papa "
        "s'accroupit. Il veut la haute tout de suite. Question. Il saute, "
        "les mains se heurtent, Nina dit non. Il refuse de foncer, écoute, "
        "retrouve l'éclat, cueille bas, fait rouler. Nina laisse tomber "
        "une haute. Merci vécu. Vers le plaid, il porte trop haut : une "
        "fraise roule. Il refuse, tient le fond, Nina le bord. Sur le "
        "plaid, basse qui roule, haute qui tombe. L'éclat d'émail tient. "
        "Goutte de jus au bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : eau froide, bol émaillé, torchon bleu, terre tiède, "
        "cerisier, plaid rêche, fraisiers, feuilles râpeuses.\n"
        "- Désir : un bol de fraises **maintenant**, avec Nina, pour le "
        "goûter sur le plaid.\n"
        "- Objet : bol émaillé, fraises hautes et basses, plaid.\n"
        "- Indice unique : éclat d'émail, vu dès l'ouverture, payé sur le "
        "bol.\n"
        "- Urgence douce : le goûter attend, Nina vient d'arriver, une "
        "haute est trop haut.\n"
        "- Imprévu 1 : il lève trop haut ; le bol penche ; l'éclat saute ; "
        "il saute, les mains se heurtent.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après le regard jusqu'au bout.\n"
        "- Imprévu 2 (plus rusé) : porter le bol trop haut ; une fraise "
        "roule ; Nina reprend d'un coup, l'autre côté penche.\n"
        "- Résolution : bouche de l'élan fermée, basse qui roule, fond "
        "tenu, bord tenu plus haut.\n"
        "- Retour : bol plus froid, goutte de jus, éclat qui tient.\n\n"
        "## Vécu\n\n"
        "Victorino veut les fraises **maintenant**, avec Nina. Impatience, "
        "puis épaules qui tombent quand la haute reste trop haut. Papa "
        "s'accroupit, pose une question, ne récite pas la règle. "
        "Victorino agit : il refuse de foncer, cueille bas, tient le "
        "fond. Nina garde les hautes, le bord. Merci vécu après le regard "
        "jusqu'au bout. Fin : l'éclat du début tient sur le bol.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau « Le bol de fraises » (dump). Monde dump : jardin, "
        "fraisiers, plaid sous le cerisier, bol émaillé.\n"
        "- Ouverture inventée (eau qui glisse, bol du robinet, éclat "
        "d'émail), pas gabarit v2, pas « joue au salon ». Craft example4 "
        "(093, 025, 057) : sourire qui disparaît, refuse de foncer, "
        "indice payé.\n"
        "- Distinct de DIF.COR.001-02.. (carton, bateaux, drap). Ici : "
        "jouer grand/petit, vécu jardin et fraises.\n"
        "- Papa ajouté. Nina = copine (oui, non, silence, ding). Pas "
        "« vous jouez ensemble / petit ou grand / tailles différentes ».\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel.\n"
        "- Pas éclat de fraise (BAN), pas enveloppe, dalle, plaque, "
        "pierre, grille, couvercle, cheminée.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat d'émail » nommé à l'ouverture, revu "
        "quand il saute, revu sur le bord, payé à la fin.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
