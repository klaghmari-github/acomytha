#!/usr/bin/env python3
"""TREE-AUT-022 — La pomme dans l'herbe (F-NAR-019, N3, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-022"
N3 = LIMITS["N3"]
TITLE = "La pomme dans l'herbe"
CHILD = "enfant-m"
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
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="feuille-œil",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=le_saladier_vide_attend_la_quatrieme; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note=(
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton_choix_change_la_maniere; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="manteau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=les_epaules_ont_pris_la_laine; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; intensite=1; "
            "destinataire=enfant; sous_texte=le_toc_dit_que_les_manches_sont_enfilees; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_pomme_sans_le_manteau; "
            "tempo=vif; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=un_faux_rouge_ment_la_feuille_oeil_dit_vrai; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="feuille-œil",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=il_regarde_par_le_trou_sans_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="saladier",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=la_feuille_oeil_et_le_toc_ont_tenu_promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | le manteau | son manteau | le manteau bleu | le manteau de laine",
    "retry_prompt": "Le manteau bleu. Aniss a mis quoi ?",
}

LOC = {
    1: dict(name="la cuisine", short="cuisine", sons="saladier,casserole,four"),
    2: dict(name="le jardin", short="jardin", sons="herbe,pommier,vent"),
    3: dict(name="la chambre", short="chambre", sons="rideau,panier,tapis"),
}
OBJ = {
    1: dict(name="les cubes", short="cubes", un="un cube", sons="cubes,bois"),
    2: dict(name="le livre", short="livre", un="le livre", sons="pages,livre"),
    3: dict(name="la dînette", short="dînette", un="une tasse", sons="tasse,assiette"),
}
MOM = {
    1: dict(name="le matin", short="matin", sons="rosée,pommier"),
    2: dict(name="après la sieste", short="sieste", sons="soleil,fenetre"),
    3: dict(name="le soir", short="soir", sons="lampe,crochet"),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
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
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms", "night_policy", "fields"):
            continue
        out[k] = v
    return out


def path_ids(a: int, b: int, c: int) -> list[str]:
    return [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        f"CHK_T0001_P000{a}",
        f"CHK_T0001_P000{a}_Q0001",
        f"CHK_T0001_P000{a}_C0001",
        f"CHK_T0001_P000{a}_T0002_P0000",
        f"CHK_T0001_P000{a}_T0002_P000{b}",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001",
    ]


OPENING = [
    "narrateur|La porte de la cuisine laisse passer une odeur de pâte.",
    "narrateur|Un saladier blanc attend, vide, au milieu de la table.",
    "papa|Il manque la quatrième pomme, Aniss.",
    "maman|Le four chauffe, le plat ne peut pas attendre.",
    "narrateur|Dehors, le pommier penche au-dessus de l'herbe.",
    "narrateur|Une pomme rouge brille, tombée, un peu lourde.",
    "narrateur|Une feuille collée dessus a un petit trou rond.",
    "narrateur|Sur le banc du pommier, un manteau bleu attend.",
    "narrateur|En ce moment, Aniss court vers l'herbe, trop vite.",
    "enfant-m|Je la prends, pour la tarte !",
    "narrateur|Il attrape le manteau d'une main, sans l'enfiler.",
    "narrateur|La manche se tord, le tissu tombe dans l'herbe.",
    "enfant-m|Il est mouillé, il me ralentit !",
    "narrateur|Ses épaules baissent, un instant, près du banc.",
    "narrateur|L'herbe froide pique ses poignets nus.",
    "papa|Regarde la feuille-œil, sur la pomme.",
    "maman|Le manteau d'abord, puis le fruit.",
]

T1_CHOICE = [
    "narrateur|Le four attend, et la pomme aussi.",
    "papa|On passe où, avant de la porter ?",
    "maman|La cuisine, le jardin, ou la chambre.",
]

T1 = {
    1: [
        "narrateur|Aniss pousse la porte du coin de la tarte.",
        "narrateur|Le saladier vide brille, trop propre.",
        "enfant-m|La pomme va ici, tout de suite !",
        "narrateur|Il jette le manteau sur une chaise, pressé.",
        "narrateur|La manche accroche le dos de bois.",
        "narrateur|Une cuillère tombe, clac, au sol.",
        "enfant-m|Ça m'empêche d'y aller !",
        "narrateur|Ses poings se serrent, près du saladier.",
        "papa|Le four attend, pas tes épaules nues.",
        "maman|Le manteau, vois, il a glissé.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "narrateur|Aniss souffle, les joues chaudes.",
        "enfant-m|Je le mets, alors.",
        "narrateur|Il glisse un bras, puis l'autre, plus lent.",
        "narrateur|Un bouton de bois fait toc, contre lui.",
    ],
    2: [
        "narrateur|Aniss court vers le banc du pommier.",
        "narrateur|L'herbe mouillée brille, froide, un peu haute.",
        "narrateur|La pomme rouge attend, sous la feuille-œil.",
        "enfant-m|Je la prends, sans le manteau !",
        "narrateur|Il court, le tissu à la main, trop vite.",
        "narrateur|Une botte glisse, la pomme roule plus loin.",
        "narrateur|Le manteau tombe, lourd, dans l'herbe.",
        "enfant-m|Je n'y arrive pas.",
        "narrateur|Son sourire disparaît, près de l'arbre.",
        "papa|Tes poignets sont nus, Aniss.",
        "maman|Le manteau, vois, il fume un peu.",
        "narrateur|Papa s'accroupit, près de l'herbe.",
        "enfant-m|Il est froid, et lourd.",
        "narrateur|Il enfile les manches, malgré la hâte.",
        "narrateur|Un bouton de bois fait toc, contre lui.",
    ],
    3: [
        "narrateur|Aniss entre dans la chambre, pour le panier.",
        "narrateur|Par la fenêtre, la pomme brille dans l'herbe.",
        "enfant-m|Je prends le panier, et je cours !",
        "narrateur|Il pose le manteau sur le lit, trop vite.",
        "narrateur|Le panier est vide, léger, sans fruit.",
        "narrateur|Un air froid vient de la fenêtre.",
        "enfant-m|Il manque la pomme, ici aussi.",
        "narrateur|Ses épaules se serrent, sans laine.",
        "maman|Le panier attend un fruit, et tes bras au chaud.",
        "papa|Le manteau, vois, sur la couverture.",
        "narrateur|Maman s'accroupit, près du tapis.",
        "narrateur|Aniss reprend le tissu, un peu rêche.",
        "enfant-m|Je le mets, pour sortir.",
        "narrateur|Il glisse les manches, plus lent.",
        "narrateur|Un bouton de bois fait toc, contre lui.",
    ],
}

T1_Q = {
    1: [
        "narrateur|Aniss n'a plus les poignets nus, dans la cuisine.",
        "papa|Il a mis quoi, pour l'herbe ?",
    ],
    2: [
        "narrateur|Dehors, Aniss n'a plus les poignets nus.",
        "maman|Il a mis quoi, avant la pomme ?",
    ],
    3: [
        "narrateur|Le manteau frotte la porte de la chambre.",
        "papa|Aniss a mis quoi ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Le manteau bleu tient ses épaules, chaud.",
        "enfant-m|Je peux porter la pomme, maintenant.",
        "papa|Merci, Aniss, tes bras sont prêts.",
        "maman|Le saladier t'attend, avec le fruit.",
        "narrateur|La cuillère de bois est ramassée.",
        "enfant-m|Je l'emporte, pour la tarte.",
        "papa|On prend un jeu, avant le four ?",
        "narrateur|Un toc minuscule répond, près du col.",
    ],
    2: [
        "narrateur|Le manteau bleu tient ses épaules, dehors.",
        "enfant-m|Je peux chercher la pomme, maintenant.",
        "maman|Merci, Aniss, tes bras sont au chaud.",
        "papa|L'herbe mouille moins, avec la laine.",
        "narrateur|Une goutte glisse du bas du manteau.",
        "enfant-m|Elle est loin, la pomme.",
        "maman|On prend un jeu, sous le pommier ?",
        "narrateur|Un toc minuscule répond, près du col.",
    ],
    3: [
        "narrateur|Le manteau bleu tient ses épaules, dans la chambre.",
        "enfant-m|Le panier est prêt, moi aussi.",
        "papa|Merci, Aniss, tes bras sont au chaud.",
        "maman|La fenêtre montre l'herbe, et le fruit.",
        "narrateur|Le panier vide tape sa hanche, léger.",
        "enfant-m|On va la chercher.",
        "papa|On prend un jeu, avec le panier ?",
        "narrateur|Un toc minuscule répond, près du col.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près du saladier, un jeu l'appelle.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Le manteau reste avec toi.",
    ],
    2: [
        "narrateur|Près du pommier, un jeu l'appelle.",
        "maman|Les cubes, le livre, ou la dînette ?",
        "papa|Le manteau reste avec toi.",
    ],
    3: [
        "narrateur|Près du panier, un jeu l'appelle.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Le manteau reste avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Aniss prend les cubes, près du saladier.",
            "narrateur|Ils sont en bois, un peu lourds.",
            "enfant-m|Je fais un socle, pour la pomme !",
            "narrateur|Il empile trop vite, la tour penche.",
            "narrateur|Un cube rouge roule vers le saladier.",
            "enfant-m|La pomme, elle est revenue !",
            "narrateur|Il saisit le cube, dur, sans feuille.",
            "enfant-m|Ce n'est pas elle.",
            "narrateur|Son sourire disparaît, un instant.",
            "papa|Personne ne te dit où chercher.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Il écoute la casserole, le four, la porte.",
            "narrateur|Près du seuil, un trou de lumière tremble.",
            "enfant-m|La feuille-œil, comme sous l'arbre.",
        ],
        (1, 2): [
            "narrateur|Aniss ouvre le livre, près du saladier.",
            "narrateur|Une page montre un fruit rouge, plat.",
            "enfant-m|Elle est là, dans le livre !",
            "narrateur|Il pose la page dans le saladier, trop vite.",
            "narrateur|Le papier se recourbe, vide, sans poids.",
            "enfant-m|Ce n'est qu'une image.",
            "narrateur|Dans sa poitrine, ça tape trop vite.",
            "maman|Le four n'attend pas une image.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "papa|Personne ne te dit le chemin.",
            "narrateur|Il écoute la pâte, qui chante un peu.",
            "narrateur|Sur la vitre, un rond de lumière perce.",
            "enfant-m|Le trou de la feuille, dehors.",
            "narrateur|La page rouge reste ouverte, sans fruit.",
        ],
        (1, 3): [
            "narrateur|Aniss prend la dînette, près du saladier.",
            "narrateur|Une petite tasse sonne, creuse.",
            "enfant-m|Je sers la pomme, tout de suite !",
            "narrateur|Il pose un fruit en bois dans l'assiette.",
            "narrateur|Le fruit jouet roule, trop léger.",
            "enfant-m|Ce n'est pas la vraie.",
            "narrateur|Ses mains s'arrêtent, au-dessus de la tasse.",
            "papa|Personne ne te dit où elle s'est cachée.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Il écoute le four, qui souffle bas.",
            "narrateur|Un rond de lumière tremble près de la porte.",
            "enfant-m|La feuille-œil, je la vois.",
            "maman|Le manteau t'y mène, dehors.",
            "narrateur|La petite assiette reste vide, vraie.",
        ],
        (2, 1): [
            "narrateur|Aniss pose les cubes sous le pommier.",
            "narrateur|L'herbe mouille le bois, un peu.",
            "enfant-m|Je monte, je l'attrape !",
            "narrateur|La tour penche, un cube rouge tombe.",
            "narrateur|Dans l'herbe, le cube brille, comme un fruit.",
            "enfant-m|La pomme !",
            "narrateur|Sa main touche le bois, pas la peau.",
            "enfant-m|Ce n'est pas elle.",
            "narrateur|Ses épaules baissent, près du banc.",
            "papa|Personne ne te dit de courir.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Il écoute l'herbe, le vent, l'arbre.",
            "narrateur|Un petit trou rond perce une feuille, plus loin.",
            "enfant-m|La feuille-œil, elle a bougé.",
        ],
        (2, 2): [
            "narrateur|Aniss ouvre le livre, sous le pommier.",
            "narrateur|Une page rouge tremble au vent.",
            "enfant-m|Je couvre la pomme, pour la voir !",
            "narrateur|Il pose le livre trop vite, sur l'herbe.",
            "narrateur|La page cache un reflet, pas le fruit.",
            "enfant-m|Elle n'est plus là.",
            "narrateur|Son sourire disparaît, près des racines.",
            "maman|Personne ne te dit de soulever trop fort.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Il écoute les feuilles, au-dessus.",
            "papa|Regarde, pas l'image.",
            "narrateur|Un trou rond laisse passer le ciel, plus loin.",
            "enfant-m|La feuille-œil, sous l'arbre.",
            "narrateur|Le livre garde une goutte, sur la page.",
        ],
        (2, 3): [
            "narrateur|Aniss pose la dînette dans l'herbe.",
            "narrateur|La petite assiette est froide, vide.",
            "enfant-m|Je l'y mets, la pomme !",
            "narrateur|Il ramasse trop vite un fruit d'herbe ronde.",
            "narrateur|C'est une boule de terre, pas la pomme.",
            "enfant-m|Elle m'a trompé.",
            "narrateur|Dans sa poitrine, l'envie se bouscule.",
            "papa|Personne ne te dit de foncer.",
            "narrateur|Aniss s'arrête, les mains sales.",
            "narrateur|Il écoute l'arbre, un toc de bouton.",
            "narrateur|Un petit trou rond brille, plus bas.",
            "enfant-m|La feuille-œil, je la vois.",
            "maman|Le manteau te tient, pendant que tu regardes.",
            "narrateur|La petite tasse reste vide, dans l'herbe.",
        ],
        (3, 1): [
            "narrateur|Aniss pose les cubes près du panier.",
            "narrateur|Le tapis étouffe le bruit du bois.",
            "enfant-m|Je fais un chemin, jusqu'à la pomme !",
            "narrateur|La tour tombe vers la fenêtre, trop vite.",
            "narrateur|Un cube rouge s'allume dans le verre.",
            "enfant-m|Elle est dehors, je la vois !",
            "narrateur|C'est le cube, reflété, pas le fruit.",
            "enfant-m|Le verre a menti.",
            "narrateur|Ses épaules baissent, près du lit.",
            "papa|Personne ne te dit de courir sans regarder.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Il écoute le rideau, le vent, le jardin.",
            "narrateur|Par le verre, un trou rond perce une feuille.",
            "enfant-m|La feuille-œil, sous le pommier.",
        ],
        (3, 2): [
            "narrateur|Aniss ouvre le livre, sur le lit.",
            "narrateur|Une page montre un arbre, et un fruit.",
            "enfant-m|Je compare, je la trouve !",
            "narrateur|Il colle la page à la fenêtre, trop vite.",
            "narrateur|L'image cache le jardin, un instant.",
            "enfant-m|Je ne vois plus rien.",
            "narrateur|Son sourire disparaît, contre le verre.",
            "maman|Personne ne te dit de coller la page.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Il baisse le livre, écoute la chambre.",
            "papa|Le jardin parle, derrière la vitre.",
            "narrateur|Un trou rond perce une feuille, dehors.",
            "enfant-m|La feuille-œil, je la vois.",
            "narrateur|La page se recourbe, sans pomme.",
        ],
        (3, 3): [
            "narrateur|Aniss pose la dînette près du panier.",
            "narrateur|La petite tasse sonne, contre le bois.",
            "enfant-m|Je sers le fruit, dans le panier !",
            "narrateur|Il y glisse un bouton de dînette, trop vite.",
            "narrateur|Le bouton rouge brille, comme une pomme.",
            "enfant-m|Ce n'est pas elle.",
            "narrateur|Ses mains s'arrêtent, au bord du panier.",
            "papa|Personne ne te dit de remplir avec un jouet.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Il écoute la fenêtre, un oiseau, l'herbe.",
            "narrateur|Dehors, un petit trou rond tremble.",
            "enfant-m|La feuille-œil, sous l'arbre.",
            "maman|Le manteau t'y mène, quand tu seras prêt.",
            "narrateur|Le bouton rouge reste dans la tasse, faux.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|La feuille-œil attend, selon la lumière.",
        "papa|C'est quel moment, pour la pomme ?",
        "maman|Le matin, après la sieste, ou le soir.",
    ],
    2: [
        "narrateur|La feuille-œil change, selon la lumière.",
        "maman|C'est quel moment, pour la pomme ?",
        "papa|Le matin, après la sieste, ou le soir.",
    ],
    3: [
        "narrateur|La feuille-œil brille, selon la lumière.",
        "papa|C'est quel moment, pour la pomme ?",
        "maman|Le matin, après la sieste, ou le soir.",
    ],
}


TIME = {
    1: [
        "narrateur|C'est le matin, la rosée tient l'herbe.",
        "enfant-m|La pomme est froide, je la sens.",
    ],
    2: [
        "narrateur|C'est après la sieste, les joues d'Aniss sont chaudes.",
        "enfant-m|La pomme a bougé, peut-être.",
    ],
    3: [
        "narrateur|C'est le soir, une lampe fait un rond jaune.",
        "enfant-m|Je la vois moins, je dois regarder.",
    ],
}

SEARCH = {
    (1, 1): [
        "narrateur|Aniss sort par la porte de la cuisine, manteau boutonné.",
        "narrateur|Il ralentit, près du saladier vide, puis dehors.",
        "narrateur|La rosée a rempli le trou de la feuille.",
        "enfant-m|Un rond brillant, comme un œil.",
        "narrateur|Il s'accroupit, sans foncer.",
        "narrateur|Par le trou, le rouge de la pomme apparaît.",
    ],
    (1, 2): [
        "narrateur|Aniss quitte le coin de la tarte, manteau boutonné.",
        "narrateur|Le soleil pose un rond sur le carrelage, puis l'herbe.",
        "narrateur|Le trou de la feuille dessine une ombre ronde.",
        "enfant-m|L'ombre mène, pas le cube.",
        "narrateur|Il suit l'ombre, pas à pas.",
        "narrateur|Sous la feuille, le fruit attend, tiède.",
    ],
    (1, 3): [
        "narrateur|Aniss quitte la cuisine, manteau boutonné, lent.",
        "narrateur|La lampe de la table perce le trou, dehors.",
        "narrateur|Un point rouge s'allume, dans l'herbe sombre.",
        "enfant-m|C'est elle, pas la tasse.",
        "narrateur|Il s'approche, sans courir.",
        "narrateur|La pomme est là, sous la feuille-œil.",
    ],
    (2, 1): [
        "narrateur|Aniss reste sous le pommier, manteau boutonné.",
        "narrateur|La rosée tient le trou, comme une loupe.",
        "narrateur|Il se baisse, les genoux dans l'herbe froide.",
        "enfant-m|Je regarde par le trou, pas à côté.",
        "narrateur|Le rouge apparaît, net, au centre.",
        "narrateur|La pomme n'a pas fui, elle attendait.",
    ],
    (2, 2): [
        "narrateur|Aniss reste sous le pommier, manteau boutonné.",
        "narrateur|Le soleil a séché le trou, il est net.",
        "narrateur|Une ombre ronde glisse sur l'herbe chaude.",
        "enfant-m|Je suis l'ombre, pas le reflet.",
        "narrateur|Il avance lentement, vers le banc.",
        "narrateur|Sous une feuille, le fruit est tiède.",
    ],
    (2, 3): [
        "narrateur|Aniss reste sous le pommier, manteau boutonné.",
        "narrateur|La lumière de la maison perce le trou.",
        "narrateur|Un œil rouge s'allume, près des racines.",
        "enfant-m|Je vais là, sans courir.",
        "narrateur|L'herbe est froide, le fruit est lourd.",
        "narrateur|La feuille-œil repose sur la pomme, fidèle.",
    ],
    (3, 1): [
        "narrateur|Aniss ouvre la fenêtre de la chambre, manteau boutonné.",
        "narrateur|La rosée du matin brille, dans le trou.",
        "narrateur|Il descend avec le panier, pas à pas.",
        "enfant-m|Je regarde par le trou, depuis le seuil.",
        "narrateur|Le rouge apparaît, entre deux brins.",
        "narrateur|La pomme attend, près du banc.",
    ],
    (3, 2): [
        "narrateur|Aniss quitte la chambre, manteau boutonné, panier à la main.",
        "narrateur|Le soleil de la sieste perce le rideau, puis le trou.",
        "narrateur|Une ombre ronde tombe sur l'herbe sèche.",
        "enfant-m|L'ombre, pas le reflet du verre.",
        "narrateur|Il suit l'ombre jusqu'au pommier.",
        "narrateur|La pomme est tiède, sous la feuille-œil.",
    ],
    (3, 3): [
        "narrateur|Aniss quitte la chambre, manteau boutonné, veilleuse derrière.",
        "narrateur|La lampe du salon perce le trou, dehors.",
        "narrateur|Un point rouge s'allume, près du banc sombre.",
        "enfant-m|Je vais là, le panier ouvert.",
        "narrateur|Il s'accroupit, sans foncer.",
        "narrateur|La pomme est là, sous la feuille-œil.",
    ],
}

TOOL = {
    1: [
        "narrateur|Un cube soulève la feuille, sans l'écraser.",
        "enfant-m|Je la prends à deux mains, elle est lourde.",
        "narrateur|La peau est lisse, un peu froide.",
    ],
    2: [
        "narrateur|Le livre fait un toit, pour qu'elle ne roule pas.",
        "enfant-m|Je la prends à deux mains, elle est lourde.",
        "narrateur|La peau est lisse, un peu froide.",
    ],
    3: [
        "narrateur|La petite tasse l'accueille, le temps d'un souffle.",
        "enfant-m|Je la prends à deux mains, elle est lourde.",
        "narrateur|La peau est lisse, un peu froide.",
    ],
}

PAY = {
    (1, 1, 1): [
        "narrateur|Il pose la pomme dans le saladier, près d'un cube.",
        "narrateur|La feuille-œil reste au bord, trou vers le four.",
        "maman|Tu l'as portée, sans foncer.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 1, 2): [
        "narrateur|Il pose la pomme dans le saladier, un cube à côté.",
        "narrateur|Une goutte de rosée sèche sur le bois du cube.",
        "papa|Tu l'as vue par le trou, pas par le cube.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 1, 3): [
        "narrateur|Il pose la pomme dans le saladier, sous la lampe.",
        "narrateur|Le trou de la feuille reflète le rond jaune.",
        "maman|Le four peut attendre une minute, maintenant.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 2, 1): [
        "narrateur|Il pose la pomme dans le saladier, le livre ouvert.",
        "narrateur|Une page sent la pâte, près du fruit.",
        "papa|L'image n'était pas elle.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 2, 2): [
        "narrateur|Il pose la pomme dans le saladier, le livre tiède.",
        "narrateur|La vitre embuée garde un rond, comme le trou.",
        "maman|Tu as regardé dehors, pas la page.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 2, 3): [
        "narrateur|Il pose la pomme dans le saladier, le livre fermé.",
        "narrateur|La lampe dore le bord d'une page, et le trou.",
        "papa|Le fruit a son vrai poids, pas le papier.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 3, 1): [
        "narrateur|Il pose la pomme dans le saladier, la tasse à côté.",
        "narrateur|Une goutte de rosée perle au bord de la tasse.",
        "maman|La vraie a rempli le blanc.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 3, 2): [
        "narrateur|Il pose la pomme dans le saladier, l'assiette miniature près.",
        "narrateur|La dînette est chaude, comme la casserole.",
        "papa|Le jouet a laissé la place au fruit.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (1, 3, 3): [
        "narrateur|Il pose la pomme dans le saladier, la petite cuillère brille.",
        "narrateur|Le trou de la feuille s'allume sous la lampe.",
        "maman|Le saladier n'est plus vide.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 1, 1): [
        "narrateur|Il porte la pomme vers la cuisine, un cube dans l'autre main.",
        "narrateur|Une feuille d'herbe reste collée au cube.",
        "papa|Tu l'as trouvée par le trou, pas par le bois.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 1, 2): [
        "narrateur|Il porte la pomme vers la cuisine, le cube tiède.",
        "narrateur|Le soleil a séché le bois, pas le fruit.",
        "maman|L'ombre ronde t'a menée.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 1, 3): [
        "narrateur|Il porte la pomme vers la cuisine, le cube sombre.",
        "narrateur|Une goutte ronde reste sur le bois, comme le trou.",
        "papa|La lumière de la maison a parlé.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 2, 1): [
        "narrateur|Il porte la pomme vers la cuisine, le livre sous le bras.",
        "narrateur|Une vraie feuille marque la page, trou compris.",
        "maman|La page n'était qu'une image.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 2, 2): [
        "narrateur|Il porte la pomme vers la cuisine, le livre sent l'herbe.",
        "narrateur|Une goutte sèche au bord de la page.",
        "papa|Tu as suivi l'ombre, pas le vent.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 2, 3): [
        "narrateur|Il porte la pomme vers la cuisine, le livre fermé.",
        "narrateur|Un oiseau se tait, près du banc.",
        "maman|Le trou a gardé le rouge, malgré la nuit.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 3, 1): [
        "narrateur|Il porte la pomme vers la cuisine, l'assiette miniature à la main.",
        "narrateur|Un peu de rosée reste au bord de l'assiette.",
        "papa|La terre n'était pas le fruit.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 3, 2): [
        "narrateur|Il porte la pomme vers la cuisine, la tasse tiède.",
        "narrateur|La dînette a l'odeur de l'herbe chaude.",
        "maman|Tu as regardé le trou, pas la boule.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (2, 3, 3): [
        "narrateur|Il porte la pomme vers la cuisine, la tasse sombre.",
        "narrateur|Une goutte glisse du manteau, vers le sol.",
        "papa|Le toc a tenu, dehors.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 1, 1): [
        "narrateur|Il pose la pomme dans le panier, un cube contre le fruit.",
        "narrateur|Un rayon du matin dore la tour, près du lit.",
        "maman|Le panier n'est plus vide.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 1, 2): [
        "narrateur|Il pose la pomme dans le panier, un cube contre l'oreiller.",
        "narrateur|Le tapis garde une ombre ronde, comme le trou.",
        "papa|Le verre de la fenêtre avait menti.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 1, 3): [
        "narrateur|Il pose la pomme dans le panier, les cubes dans l'ombre.",
        "narrateur|La veilleuse dore le bois, et le fruit.",
        "maman|Tu as descendu les marches, sans courir.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 2, 1): [
        "narrateur|Il pose la pomme dans le panier, le livre ouvert.",
        "narrateur|Le rideau vert colore une page, et le trou.",
        "papa|La page n'a pas gagné.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 2, 2): [
        "narrateur|Il pose la pomme dans le panier, le livre sur la couverture.",
        "narrateur|Une page sent le savon, un peu.",
        "maman|L'ombre du trou t'a menée au jardin.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 2, 3): [
        "narrateur|Il pose la pomme dans le panier, le livre fermé.",
        "narrateur|La veilleuse dore le bord d'une page.",
        "papa|Le jardin a parlé, derrière la vitre.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 3, 1): [
        "narrateur|Il pose la pomme dans le panier, la tasse près du lit.",
        "narrateur|Un bouton de dînette reste dans la tasse, faux.",
        "maman|Le vrai fruit a son poids.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 3, 2): [
        "narrateur|Il pose la pomme dans le panier, la dînette au pied du lit.",
        "narrateur|La petite assiette reflète le soleil de la sieste.",
        "papa|Le jouet a cédé la place.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
    (3, 3, 3): [
        "narrateur|Il pose la pomme dans le panier, l'assiette miniature reflète la veilleuse.",
        "narrateur|Le trou de la feuille s'éteint, son travail fini.",
        "maman|Le panier tient le fruit, le crochet tient le manteau.",
        "narrateur|Aniss raccroche le manteau, toc, au crochet bas.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    return TIME[c] + SEARCH[(a, c)] + TOOL[b] + PAY[(a, b, c)]


LAST = {
    (1, 1, 1): "La feuille-œil sèche au bord du saladier, trou vers le four.",
    (1, 1, 2): "Un cube garde une goutte de rosée, ronde, près du fruit.",
    (1, 1, 3): "Le saladier reflète la lampe, dans le trou de la feuille.",
    (1, 2, 1): "Une page sent la pâte, ouverte à côté du saladier.",
    (1, 2, 2): "Le livre est tiède, sous la vitre embuée.",
    (1, 2, 3): "La lampe dore le livre fermé, et le bord du saladier.",
    (1, 3, 1): "La petite tasse sèche près de l'évier, sans fruit jouet.",
    (1, 3, 2): "La casserole fait un petit pschitt, le saladier est plein.",
    (1, 3, 3): "Le bouton de bois du manteau brille, au crochet bas.",
    (2, 1, 1): "Une feuille d'herbe reste collée à un cube, sur la table.",
    (2, 1, 2): "Le cube sèche au soleil, un peu vert, près de la fenêtre.",
    (2, 1, 3): "Une goutte glisse du manteau, jusqu'au carrelage.",
    (2, 2, 1): "Une vraie feuille, trou compris, reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre, sans pomme.",
    (2, 2, 3): "La pomme ne brille plus dehors, elle est dans le blanc.",
    (2, 3, 1): "La petite assiette a de la rosée, au bord.",
    (2, 3, 2): "Un oiseau s'en va, loin du banc du pommier.",
    (2, 3, 3): "Le col bleu sèche, au crochet, sans goutte.",
    (3, 1, 1): "Le panier repose près d'un cube, le fruit dedans.",
    (3, 1, 2): "L'oreiller sent le savon, le panier sent le fruit.",
    (3, 1, 3): "Le rideau vert ne bouge plus, la pomme est rentrée.",
    (3, 2, 1): "Le panier sèche sur la couverture, une page à côté.",
    (3, 2, 2): "Une page reste ouverte, sur le lit, sans image de fruit.",
    (3, 2, 3): "La veilleuse dore le livre, et le crochet.",
    (3, 3, 1): "La petite tasse est près du panier, le bouton jouet dedans.",
    (3, 3, 2): "Le tapis de la chambre est calme, le fruit est parti.",
    (3, 3, 3): "La pomme attend dans le saladier, le panier s'est vidé.",
}


def ending_lines(a: int, b: int, c: int) -> list[str]:
    loc = LOC[a]["name"]
    obj = OBJ[b]["name"]
    mom = MOM[c]["name"]
    qs = {
        1: "papa|Tu raconteras le moment difficile, Aniss ?",
        2: "maman|Tu raconteras le moment difficile, Aniss ?",
        3: "papa|Tu raconteras le trou dans la feuille ?",
    }[c]
    ans = {
        1: "enfant-m|Surtout celui-là, près du saladier.",
        2: "enfant-m|Surtout celui-là, sous le pommier.",
        3: "enfant-m|Surtout le trou, et le toc.",
    }[c]
    return [
        "narrateur|La pâte sent plus fort, dans la cuisine.",
        f"narrateur|Aniss est passé par {loc}.",
        f"narrateur|Il a emporté {obj}.",
        f"narrateur|C'était {mom}.",
        "narrateur|Le manteau bleu retrouve le crochet bas.",
        "enfant-m|La quatrième pomme est arrivée.",
        qs,
        ans,
        "maman|Le saladier n'est plus vide, maintenant.",
        "enfant-m|La feuille-œil a aidé.",
        f"narrateur|{LAST[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{LOC[a]['short']}_{OBJ[b]['short']}_{MOM[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "pommier,pate,manteau,saladier")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "la cuisine",
            "option_2_label": "le jardin",
            "option_3_label": "la chambre",
        }},
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            LOC[a]["sons"],
            {"emphasis": LOC[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": "manteau", "fields": Q_FIELDS},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            LOC[a]["sons"],
            {"emphasis": "manteau"},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "les cubes",
                "option_2_label": "le livre",
                "option_3_label": "la dînette",
            }},
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                OBJ[b]["sons"],
                {"emphasis": OBJ[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le matin",
                    "option_2_label": "après la sieste",
                    "option_3_label": "le soir",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    MOM[c]["sons"],
                    {"emphasis": "feuille-œil"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "saladier,crochet,pate",
                    {"emphasis": "saladier", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = [out_chunks[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    lasts = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in out_chunks[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage"
        and "T0003_P000" in c["chunk_id"]
        and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    t2_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "_T0002_P000" in c["chunk_id"] and "T0003" not in c["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Le saladier blanc attend, vide : il manque la quatrième pomme. "
        "Elle brille dans l'herbe, une feuille-œil collée dessus. Aniss "
        "court trop vite, manteau bleu à la main : la manche se tord, "
        "l'herbe pique. Il enfile le manteau. Cuisine, jardin ou chambre, "
        "première idée, patatras. Cubes, livre ou dînette : un faux rouge "
        "ment, la feuille-œil dit vrai. Matin, sieste ou soir, il refuse "
        "de foncer, regarde par le trou, porte le fruit, raccroche. "
        "Le toc et le saladier paient le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Aniss, papa, maman"
    merged["setting"] = "jardin du pommier, coin de la tarte, cuisine, jardin ou chambre"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    if min(counts) < 550 or max(counts) > 700:
        raise SystemExit(f"chemin hors barre 550-700: min {min(counts)} max {max(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019. Graphe, `chunk_id`, types de blocs "
        "et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La pâte sent, le saladier blanc est vide : il manque la quatrième "
        "pomme. Sous le pommier, une pomme rouge porte une feuille-œil "
        "(trou rond). Un manteau bleu à boutons de bois attend sur le banc. "
        "Aniss court trop vite, sans l'enfiler : la manche se tord, l'herbe "
        "pique. Cuisine, jardin ou chambre, il met le manteau. Cubes, livre "
        "ou dînette : un faux rouge ment. Matin, sieste ou soir, il refuse "
        "de foncer, regarde par le trou, porte le fruit, raccroche. Le toc "
        "et le saladier paient le début.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin du pommier, coin de la tarte, saladier vide.\n"
        "- Désir : porter la quatrième pomme avant que le four n'attende trop.\n"
        "- Objet : pomme rouge à feuille-œil, manteau bleu (toc), plus cubes / livre / dînette.\n"
        "- Urgence douce : le plat ne peut pas attendre.\n"
        "- Imprévu 1 : manteau mal pris, herbe froide, pomme qui roule.\n"
        "- Cue : enfiler le manteau, regarder le trou. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : un faux rouge (cube, image, jouet) ment ; la feuille-œil dit vrai.\n"
        "- Résolution : refuser de foncer, regarder par le trou, selon la lumière.\n"
        "- Retour : toc, saladier plein, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Le premier choix n'enlève pas le manteau : il vient jusqu'à la pomme.\n"
        "- Déclencheur : un ingrédient manque (la quatrième pomme, le saladier vide).\n"
        "- Neuf fausses pommes distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.002 vécue (mettre le manteau pour sortir), jamais dite.\n"
        "- Pas de refrain example3/v2, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Aniss, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience au départ, petit découragement quand le manteau résiste "
        "ou qu'un faux rouge ment, fierté calme quand Aniss regarde par le "
        "trou et porte le fruit. L'adulte guide peu. `slow` réservé aux choix, "
        "à la question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N3 ≤ 16 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} chemins {min(counts)}-{max(counts)} moy {sum(counts)//27}")


if __name__ == "__main__":
    build()
