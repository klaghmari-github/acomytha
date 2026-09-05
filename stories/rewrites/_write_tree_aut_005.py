#!/usr/bin/env python3
"""TREE-AUT-005 — Le coq et les bottes de Raphaël (F-NAR-019, N1, AUT.ROU.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-005"
N1 = LIMITS["N1"]
TITLE = "Le coq et les bottes de Raphaël"
CHILD = "enfant-m"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="volet bleu",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_coq_s_est_tu_il_faut_y_aller; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_recherche; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="bottes",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=les_pieds_nus_n_aiment_pas_la_boue; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="bottes",
        note="arc=confirmation; intention=relancer; emotion=soulagement_prudent; intensite=1; destinataire=enfant; sous_texte=gauche_puis_droite_le_chemin_tient; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_sort_trop_vite_sans_les_bottes; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=l_animal_fait_autre_chose_que_prévu; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="coq",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=il_comprend_sans_forcer_le_coq; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="bottes",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_toc_du_volet_a_trouvé_le_coq; tempo=posé; sourire=léger; respiration=ample",
    ),
}

Q_FIELDS = {
    "expected_answer": "les bottes",
    "accepted_examples": (
        "les bottes | bottes | ses bottes | les bottes d'abord | "
        "mettre les bottes | les bottes de Raphaël"
    ),
    "retry_prompt": "Il met les bottes. Raphaël met quoi ?",
    "engine_ok_text": "Oui, les bottes.",
    "engine_near_text": "Tu es tout près. Écoute l'indice.",
}

OBJ = {
    1: dict(name="le ballon rouge", short="ballon", sons="ballon,porte"),
    2: dict(name="le seau bleu", short="seau", sons="seau,grain"),
    3: dict(name="le doudou", short="doudou", sons="doudou,porte"),
}
ANI = {
    1: dict(name="le chat", short="chat", sons="chat,paille"),
    2: dict(name="le chien", short="chien", sons="chien,boue"),
    3: dict(name="la poule", short="poule", sons="poule,cailloux"),
}
LIEU = {
    1: dict(name="le secret du cabanon", short="cabanon", sons="loquet,coq"),
    2: dict(name="le fournil", short="fournil", sons="four,farine"),
    3: dict(name="les tomates", short="tomates", sons="feuilles,tomate"),
}


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
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms", "night_policy"):
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
    "narrateur|La ferme sent le foin, après la pluie.",
    "narrateur|Un volet bleu tape, toc, toc.",
    "narrateur|La paille brille sous la fenêtre.",
    "narrateur|Le lait fume dans le bol.",
    "maman|Le lait est prêt, Raphaël.",
    "papa|Tu as entendu le coq ?",
    f"{CHILD}|Une fois, derrière la grange.",
    "narrateur|Puis le chant s'est arrêté.",
    "narrateur|Le chemin de terre est mouillé.",
    "narrateur|Ça sent la boue et le foin.",
    "narrateur|Les bottes attendent près de la porte.",
    "narrateur|Une paille dépasse de la botte gauche.",
    "narrateur|En ce moment, Raphaël se lève.",
    "narrateur|Le plancher pique ses pieds, froid.",
    f"{CHILD}|Je veux le coq, vite !",
    "maman|Il s'est caché, après son cri.",
    "papa|Le chemin colle sous tes pieds.",
    f"{CHILD}|J'y vais, il m'attend !",
    "narrateur|Raphaël court vers la porte.",
    "narrateur|La pierre du seuil luit, glissante.",
    "narrateur|Une goutte tombe du toit, lente.",
    f"{CHILD}|Je prends un objet, pour lui.",
    "papa|Quoi, pour le chemin mouillé ?",
]

T1_CHOICE = [
    "narrateur|Raphaël peut emporter trois choses.",
    "maman|Le ballon rouge, le seau bleu, ou le doudou ?",
]

T1 = {
    1: [
        "narrateur|Raphaël saisit le ballon rouge.",
        "narrateur|Le caoutchouc est lisse, un peu tiède.",
        "narrateur|Il frotte, un petit cri de peau.",
        f"{CHILD}|Il va faire venir le coq !",
        "narrateur|Il court vers la porte, pieds nus.",
        "narrateur|Le ballon tape le bois, toc.",
        "narrateur|La porte s'ouvre sur l'air mouillé.",
        "narrateur|Le ballon glisse sur la pierre.",
        "narrateur|Il roule vers le chemin, loin.",
        f"{CHILD}|Attends !",
        "narrateur|Un chausson touche l'eau froide.",
        f"{CHILD}|Aïe, ça pique !",
        "papa|Tes pieds n'aiment pas la boue.",
        "maman|Les bottes sont là, près de toi.",
        "narrateur|La paille dépasse, comme au réveil.",
        f"{CHILD}|Le ballon est dehors, sans moi.",
        "papa|On le reprend avec les bottes ?",
    ],
    2: [
        "narrateur|Raphaël prend le seau bleu.",
        "narrateur|Le fer pèse, un peu froid.",
        "narrateur|Du grain chante au fond, chh.",
        f"{CHILD}|C'est le repas du coq !",
        "narrateur|Il marche vers la porte, vite.",
        "narrateur|Le seau tape sa jambe, clac.",
        "narrateur|La porte s'ouvre sur l'air d'étable.",
        "narrateur|Un chausson glisse sur la pierre.",
        "narrateur|Le seau penche, et deux grains tombent.",
        f"{CHILD}|Oh, le grain !",
        "narrateur|L'eau froide entre dans le tissu.",
        f"{CHILD}|Mes pieds sont glacés.",
        "maman|La pierre est trop mouillée, là.",
        "papa|Les bottes tiennent mieux, sur l'eau.",
        "narrateur|Elles attendent, une paille au bord.",
        f"{CHILD}|Je veux le chemin, et le coq.",
        "maman|Tu mets les bottes, pour le seau ?",
    ],
    3: [
        "narrateur|Raphaël serre le doudou contre lui.",
        "narrateur|Le tissu est chaud, un peu râpeux.",
        "narrateur|Il sent le lit, et le foin.",
        f"{CHILD}|Il veut voir le coq, lui aussi !",
        "narrateur|Il va vers la porte, orteils nus.",
        "narrateur|Le doudou frotte le bois, ff.",
        "narrateur|Un filet d'air froid entre.",
        "narrateur|Un orteil pose sur la pierre.",
        f"{CHILD}|Aïe, elle pique !",
        "narrateur|Une goutte mouille le doudou, vite.",
        "papa|Le chemin n'aime pas les orteils.",
        "maman|Les bottes sont près du sac.",
        "narrateur|Une paille dépasse, droite, obstinée.",
        f"{CHILD}|Le doudou a froid, moi aussi.",
        "papa|Toi d'abord, les pieds au chaud.",
        f"{CHILD}|Je mets les bottes ?",
        "maman|Tu les mets, pour le chemin ?",
    ],
}

T1_Q = {
    1: [
        "narrateur|Le ballon est sur le chemin.",
        "maman|Raphaël met quoi ?",
    ],
    2: [
        "narrateur|Le seau penche, dehors, sur l'eau.",
        "papa|Raphaël met quoi ?",
    ],
    3: [
        "narrateur|La pierre est froide, sous l'orteil.",
        "maman|Raphaël met quoi ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Raphaël pose le regard sur les bottes.",
        "narrateur|Il prend la botte gauche, d'abord.",
        "narrateur|Le caoutchouc est froid, un peu rêche.",
        "narrateur|Le pied glisse au fond, floc.",
        "narrateur|Puis la botte droite, d'un coup.",
        "narrateur|Les deux pieds sont au chaud.",
        f"{CHILD}|C'est mieux, l'eau reste dehors.",
        "maman|Merci, tes pieds sont au chaud.",
        "papa|Tu es prêt pour le chemin ?",
        f"{CHILD}|Oui, papa, le ballon m'attend.",
        "narrateur|Il marche sur la pierre, ça tient.",
        "narrateur|Il ramasse le ballon, un peu humide.",
        f"{CHILD}|On va voir qui, maintenant ?",
    ],
    2: [
        "narrateur|Raphaël pose le seau un instant.",
        "narrateur|Il prend la botte gauche, d'abord.",
        "narrateur|Le pied entre, jusqu'au talon.",
        "narrateur|Le caoutchouc serre, froid, puis tiédit.",
        "narrateur|Puis la botte droite, bien droite.",
        "narrateur|Les deux pieds sont au chaud.",
        f"{CHILD}|Le seau, maintenant, il tient.",
        "papa|Merci, tes pieds sont au chaud.",
        "maman|Tu marches sur la pierre ?",
        f"{CHILD}|Oui, maman, l'eau reste dessous.",
        "narrateur|Le seau ne penche plus, cette fois.",
        "narrateur|Deux grains restent sur le seuil.",
        f"{CHILD}|On va voir qui, avec le grain ?",
    ],
    3: [
        "narrateur|Raphaël pose le doudou sur le banc.",
        "narrateur|Il prend la botte gauche, d'abord.",
        "narrateur|Le pied entre, tout au fond.",
        "narrateur|Le caoutchouc sent le foin mouillé.",
        "narrateur|Puis la botte droite, sans se presser.",
        "narrateur|Les deux pieds sont au chaud.",
        f"{CHILD}|Le doudou, maintenant, il vient.",
        "maman|Merci, tes pieds sont au chaud.",
        "papa|Tu marches sur la pierre ?",
        f"{CHILD}|Oui, elle ne pique plus.",
        "narrateur|Il reprend le doudou, un peu humide.",
        "narrateur|La paille reste collée à la botte.",
        f"{CHILD}|On va voir qui, tous les deux ?",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Le ballon attire trois bêtes, sur le chemin.",
        "papa|Le chat, le chien, ou la poule ?",
    ],
    2: [
        "narrateur|Le grain attire trois bêtes, près de l'eau.",
        "maman|Le chat, le chien, ou la poule ?",
    ],
    3: [
        "narrateur|Le doudou intéresse trois bêtes, dehors.",
        "papa|Le chat, le chien, ou la poule ?",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    obj = OBJ[a]["name"]
    if a == 1 and b == 1:
        return [
            f"narrateur|{obj.capitalize()} tape la botte, floc.",
            "narrateur|Raphaël avance sur le chemin mouillé.",
            f"{CHILD}|Le coq est derrière la grange !",
            "narrateur|Dans la paille, un chat s'étire.",
            "narrateur|Le chat tape le ballon, vif.",
            "narrateur|Le ballon file dans une flaque.",
            f"{CHILD}|Hé, reviens !",
            "narrateur|Raphaël court, et la boue gicle.",
            "narrateur|Le chat saute plus loin, léger.",
            f"{CHILD}|Je n'y arrive pas.",
            "papa|Regarde ses pattes, pas le ballon.",
            "narrateur|Des traces vont vers trois coins.",
            "narrateur|Un toc, comme le volet bleu.",
            "maman|Il nous montre un endroit.",
            f"{CHILD}|Le coq n'est pas ici.",
        ]
    if a == 1 and b == 2:
        return [
            f"narrateur|{obj.capitalize()} rebondit contre une botte.",
            "narrateur|Près de l'étable, un chien attend.",
            f"{CHILD}|Bonjour, tu as vu le coq ?",
            "narrateur|Le chien prend le ballon, en bouche.",
            "narrateur|Le caoutchouc crie, un peu aigu.",
            f"{CHILD}|C'est à moi, lâche !",
            "narrateur|Raphaël tire, et le chien croit jouer.",
            "narrateur|Le ballon tombe, plein de boue.",
            f"{CHILD}|Il est tout sale.",
            "maman|Regarde son nez, pas tes mains.",
            "narrateur|Le nez pointe vers trois sentes.",
            "papa|Il a senti quelque chose, plus loin.",
            "narrateur|Un toc voyage, derrière la grange.",
            f"{CHILD}|Le coq n'est pas près de nous.",
        ]
    if a == 1 and b == 3:
        return [
            f"narrateur|{obj.capitalize()} roule entre les cailloux.",
            "narrateur|Dans la cour, une poule picore.",
            f"{CHILD}|Poule, tu as vu le coq ?",
            "narrateur|Elle picore le ballon, et il saute.",
            "narrateur|Raphaël tend la main, trop vite.",
            "narrateur|La poule bat des ailes, cot-cot.",
            f"{CHILD}|Elle a peur de moi.",
            "papa|Elle picore vers un côté, vois.",
            "narrateur|Trois chemins partent de la cour.",
            "narrateur|Une plume reste sur le ballon.",
            "maman|Elle nous mène, sans qu'on tire.",
            "narrateur|Un toc répond, comme le volet.",
            f"{CHILD}|Le coq s'est caché, plus loin.",
        ]
    if a == 2 and b == 1:
        return [
            f"narrateur|{obj.capitalize()} cliquette, grain au fond.",
            "narrateur|Un chat sort de la paille sèche.",
            f"{CHILD}|Du grain, pour le coq !",
            "narrateur|Le chat pousse le seau, d'une patte.",
            "narrateur|Le grain file dans la boue, chh.",
            f"{CHILD}|Non, c'est son repas !",
            "narrateur|Raphaël ramasse trop vite, ça colle.",
            f"{CHILD}|Je n'y arrive pas.",
            "maman|Regarde le poil, pas le grain.",
            "narrateur|Une paille est prise dans le poil.",
            "papa|Comme celle de ta botte, ce matin.",
            "narrateur|Le chat file vers trois coins.",
            "narrateur|Un toc, bleu, derrière un mur.",
            f"{CHILD}|Le coq n'est pas dans la boue.",
        ]
    if a == 2 and b == 2:
        return [
            f"narrateur|{obj.capitalize()} pèse, contre la jambe.",
            "narrateur|Le chien arrive, pattes mouillées.",
            f"{CHILD}|Pas le grain, c'est pour le coq !",
            "narrateur|Le chien boit l'eau du seau.",
            "narrateur|Le grain flotte, puis coule, perdu.",
            f"{CHILD}|Tu as tout mélangé !",
            "narrateur|Raphaël tire le seau, le chien joue.",
            "papa|Il a soif, pas faim de grain.",
            "narrateur|Le chien s'arrête face à trois sentes.",
            "maman|Son oreille part vers un bruit.",
            "narrateur|Un toc, comme le volet de la maison.",
            f"{CHILD}|Le coq a tapé, quelque part.",
            "narrateur|Le seau sonne, plus léger, vide.",
            f"{CHILD}|Il faut le suivre, sans crier.",
        ]
    if a == 2 and b == 3:
        return [
            f"narrateur|{obj.capitalize()} sent le grain, au fond.",
            "narrateur|Une poule saute dans le seau.",
            f"{CHILD}|Sors, c'est pour le coq !",
            "narrateur|Raphaël bascule le seau, trop fort.",
            "narrateur|La poule s'envole, et le grain s'éparpille.",
            f"{CHILD}|Zut, elle a tout pris.",
            "maman|Elle picore une ligne, vois.",
            "narrateur|Des grains mènent vers trois coins.",
            "papa|Une ligne, pas un vol, cette fois.",
            "narrateur|Un toc répond, derrière la grange.",
            f"{CHILD}|Le coq entend ça, lui aussi.",
            "narrateur|La poule s'arrête, tête de côté.",
            f"{CHILD}|Elle sait où il est.",
        ]
    if a == 3 and b == 1:
        return [
            f"narrateur|{obj.capitalize()} frotte la botte, un peu.",
            "narrateur|Un chat se jette sur le tissu.",
            f"{CHILD}|Ce n'est pas un lit !",
            "narrateur|Le chat pétrit le doudou, fort.",
            "narrateur|Raphaël tire, et le chat s'accroche.",
            f"{CHILD}|Il ne veut pas lâcher.",
            "papa|Pose-le, laisse-le finir un moment.",
            "narrateur|Le chat saute, et file plus loin.",
            "narrateur|Une paille reste sur le doudou.",
            "maman|Comme celle de ta botte, au seuil.",
            "narrateur|Trois coins s'ouvrent, derrière la grange.",
            "narrateur|Un toc, bleu, très net.",
            f"{CHILD}|Le coq n'est pas sous le chat.",
        ]
    if a == 3 and b == 2:
        return [
            f"narrateur|{obj.capitalize()} pend, contre la hanche.",
            "narrateur|Le chien veut tirer, pour jouer.",
            f"{CHILD}|Non, ce n'est pas une corde !",
            "narrateur|Raphaël tire d'un côté, trop fort.",
            "narrateur|Le doudou s'allonge, presque trop.",
            f"{CHILD}|Tu vas le déchirer !",
            "maman|Ouvre la main, il va poser.",
            "narrateur|Le chien pose, puis recule, étonné.",
            "papa|Son nez suit une odeur, plus loin.",
            "narrateur|Trois sentes sentent le foin mouillé.",
            "narrateur|Un toc voyage, comme le volet.",
            f"{CHILD}|Le coq s'est caché, je crois.",
            "narrateur|Le doudou a une trace de boue.",
        ]
    return [
        f"narrateur|{obj.capitalize()} traîne, un peu trop bas.",
        "narrateur|Une poule s'assoit dessus, comme un nid.",
        f"{CHILD}|Lève-toi, ce n'est pas pour toi !",
        "narrateur|Raphaël soulève le doudou, trop vite.",
        "narrateur|La poule picore l'air, vexée.",
        f"{CHILD}|Elle est fâchée, maintenant.",
        "papa|Elle voulait un nid, pas une bagarre.",
        "narrateur|Elle picore vers trois coins, nette.",
        "maman|Un nid, quelque part, plus calme.",
        "narrateur|Un toc, comme le volet bleu.",
        f"{CHILD}|Le coq a son secret, lui aussi.",
        "narrateur|Une plume reste sur le doudou.",
    ]


T3_CHOICE = {
    1: [
        "narrateur|Le chat regarde trois coins de ferme.",
        "papa|Le cabanon, le fournil, ou les tomates ?",
    ],
    2: [
        "narrateur|Le chien s'arrête face à trois sentes.",
        "maman|Le cabanon, le fournil, ou les tomates ?",
    ],
    3: [
        "narrateur|La poule picore vers trois coins.",
        "papa|Le cabanon, le fournil, ou les tomates ?",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    obj = OBJ[a]["name"]
    core = {
        (1, 1): [
            "narrateur|Le secret du cabanon a un loquet bleu.",
            "narrateur|Le loquet tape, toc, comme le volet.",
            "narrateur|Le chat est assis dessus, fier.",
            f"{CHILD}|Pousse-toi, le coq est dedans !",
            "narrateur|Raphaël pousse le loquet, trop vite.",
            "narrateur|Le bois claque, un cri au fond.",
            f"{CHILD}|Il a eu peur.",
            "papa|Attends, le chat descend sans toi.",
            "narrateur|Une fente reste, assez pour voir.",
        ],
        (1, 2): [
            "narrateur|Le fournil sent le pain, tout chaud.",
            "narrateur|De la farine flotte, blanche, légère.",
            "narrateur|Le chat éternue, et saute d'un sac.",
            f"{CHILD}|Le coq est sur la planche !",
            "narrateur|Raphaël tape des mains, pour l'appeler.",
            "narrateur|Un nuage blanc cache tout, un moment.",
            f"{CHILD}|Je ne le vois plus.",
            "maman|Plus de bruit, laisse la farine tomber.",
            "narrateur|Le coq est là, plumes blanches.",
        ],
        (1, 3): [
            "narrateur|La grille des tomates cliquette, fine.",
            "narrateur|Les feuilles sentent la pluie, et le vert.",
            "narrateur|Le chat chasse entre les plants.",
            f"{CHILD}|Le coq picore une tomate fendue !",
            "narrateur|Raphaël court dans le rang, trop vite.",
            "narrateur|Une tomate éclate sous la botte.",
            f"{CHILD}|C'est glissant.",
            "papa|Accroupis-toi, le rang est étroit.",
            "narrateur|Le coq recule, mais il reste.",
        ],
        (2, 1): [
            "narrateur|Le secret du cabanon sent le sac.",
            "narrateur|Le loquet bleu tape, toc, toc.",
            "narrateur|Le chien se met en travers, large.",
            f"{CHILD}|Laisse-nous entrer, je le vois !",
            "narrateur|Raphaël veut glisser, trop pressé.",
            "narrateur|Le chien bouge, et le loquet claque.",
            f"{CHILD}|Le coq a reculé, au fond.",
            "maman|Demande-lui de s'asseoir, sans crier.",
            "narrateur|Le chien s'assoit, et la fente s'ouvre.",
        ],
        (2, 2): [
            "narrateur|Le fournil souffle une chaleur ronde.",
            "narrateur|Le chien remue la queue, trop fort.",
            "narrateur|Une casserole tinte, contre la pierre.",
            f"{CHILD}|Chut, le coq est sur le pain !",
            "narrateur|Raphaël avance, la queue frappe, clang.",
            "narrateur|Le coq gonfle, et saute plus haut.",
            f"{CHILD}|Il ne veut pas descendre.",
            "papa|Le chien peut s'allonger, ici.",
            "narrateur|La queue s'arrête, et la farine retombe.",
        ],
        (2, 3): [
            "narrateur|Les tomates luisent, fendues, après l'eau.",
            "narrateur|Le chien pose une patte, trop lourde.",
            "narrateur|Une tomate s'écrase, rouge, molle.",
            f"{CHILD}|Le coq est sous la grille !",
            "narrateur|Raphaël tire le collier, un peu.",
            "narrateur|Le chien recule, et le coq s'enfonce.",
            f"{CHILD}|Il se cache davantage.",
            "maman|Une patte à la fois, plus loin.",
            "narrateur|Le chien s'assoit, hors du rang.",
        ],
        (3, 1): [
            "narrateur|Le secret du cabanon est un peu sombre.",
            "narrateur|La poule glisse la première, vive.",
            f"{CHILD}|J'entre avec elle, vite !",
            "narrateur|Raphaël pousse, et le loquet tape, toc.",
            "narrateur|Le coq picore l'air, trop près.",
            f"{CHILD}|Il n'aime pas qu'on force.",
            "papa|Laisse la poule, et toi, attends.",
            "narrateur|La poule picore, calme, au seuil.",
            "narrateur|Le coq se rapproche, un pas.",
        ],
        (3, 2): [
            "narrateur|Le fournil a une pierre tiède, au bord.",
            "narrateur|La poule picore la farine, chh.",
            f"{CHILD}|Coq, viens, c'est bon ici !",
            "narrateur|Raphaël tape des mains, trop fort.",
            "narrateur|La farine saute, et le coq cligne.",
            f"{CHILD}|Il se ferme, tout petit.",
            "maman|Plus de mains, la pierre suffit.",
            "narrateur|La poule picore, sans bruit, maintenant.",
            "narrateur|Le coq baisse une aile, moins dur.",
        ],
        (3, 3): [
            "narrateur|Les tomates sentent la feuille mouillée.",
            "narrateur|La poule picore une fente rouge.",
            f"{CHILD}|J'en prends une, pour l'appeler !",
            "narrateur|La tomate s'écrase dans la paume.",
            "narrateur|Ça glisse, et le coq recule, méfiant.",
            f"{CHILD}|Ce n'était pas une bonne idée.",
            "papa|Les mains vides d'abord, puis l'objet.",
            "narrateur|La poule reste, calme, au bout.",
            "narrateur|Le coq picore, un peu plus près.",
        ],
    }[(b, c)]
    offer = {
        1: [
            f"narrateur|Raphaël pose {obj} dans la fente.",
            "narrateur|Il ne touche pas les plumes.",
            f"{CHILD}|C'est pour toi, je reste là.",
            "narrateur|Le coq avance d'un pas, prudent.",
        ],
        2: [
            f"narrateur|Raphaël pose {obj} sur la pierre.",
            "narrateur|Un peu de grain, s'il en reste.",
            f"{CHILD}|Je ne te prends pas.",
            "narrateur|Le coq descend, une patte, puis l'autre.",
        ],
        3: [
            f"narrateur|Raphaël pose {obj} au bout du rang.",
            "narrateur|Il s'accroupit, les bottes dans la terre.",
            f"{CHILD}|Tu viens, si tu veux.",
            "narrateur|Le coq marche le rang, sans fuir.",
        ],
    }[c]
    if a == 2 and c != 2:
        offer = [
            f"narrateur|Raphaël incline {obj}, tout doucement.",
            "narrateur|Deux grains roulent, assez pour un bec.",
            f"{CHILD}|C'est ton repas, je reste là.",
            "narrateur|Le coq avance, sans être touché.",
        ]
    if a == 2 and c == 2:
        offer = [
            f"narrateur|Raphaël pose {obj} sur la pierre tiède.",
            "narrateur|Le dernier grain sonne, tout petit.",
            f"{CHILD}|Je ne te prends pas.",
            "narrateur|Le coq descend, une patte, puis l'autre.",
        ]
    clue = {
        1: "narrateur|Le loquet tape, toc, comme le volet.",
        2: "narrateur|La vapeur ressemble au lait du bol.",
        3: "narrateur|Le rouge luisant rappelle le chemin mouillé.",
    }[c]
    return core + offer + [clue, f"{CHILD}|Il est venu, tout seul."]


def ending_lines(a: int, b: int, c: int) -> list[str]:
    obj = OBJ[a]["name"]
    ani = ANI[b]["name"]
    lieu = LIEU[c]["name"]
    traces = {
        (1, 1, 1): [
            f"narrateur|{obj.capitalize()} garde une paille collée.",
            "narrateur|Le loquet bleu reste ouvert, un peu.",
            f"{CHILD}|Le chat s'est recouché, dans la paille.",
            "maman|Quel moment tu gardes, Raphaël ?",
            f"{CHILD}|Le toc, et le coq qui est venu.",
            "papa|Tes bottes ont de la boue, et une paille.",
            "narrateur|Le volet bleu répond, loin, toc.",
        ],
        (1, 1, 2): [
            f"narrateur|{obj.capitalize()} a un voile de farine.",
            "narrateur|Le chat se lèche une patte, blanche.",
            f"{CHILD}|Il a éternué, et le coq a bougé.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|La pierre tiède, et le pain autour.",
            "maman|Tes bottes sentent le four, un peu.",
            "narrateur|Le lait attend, tiède, dans le bol.",
        ],
        (1, 1, 3): [
            f"narrateur|{obj.capitalize()} porte une tache rouge, fine.",
            "narrateur|Le chat se frotte à la grille.",
            f"{CHILD}|La tomate a éclaté, sous ma botte.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Le rang, et le coq qui a marché.",
            "papa|Tes bottes ont de la terre rouge.",
            "narrateur|La grille des tomates cliquette, derrière.",
        ],
        (1, 2, 1): [
            f"narrateur|{obj.capitalize()} a une trace de dents, molle.",
            "narrateur|Le chien s'allonge au seuil du cabanon.",
            f"{CHILD}|Il a voulu entrer, trop large.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Quand il s'est assis, et le toc.",
            "maman|Tes bottes ont tenu, sur la boue.",
            "narrateur|Le secret du cabanon redevient sombre.",
        ],
        (1, 2, 2): [
            f"narrateur|{obj.capitalize()} sent le pain, et le chien.",
            "narrateur|Une casserole repose, enfin silencieuse.",
            f"{CHILD}|Sa queue a tout fait tinter.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Quand le coq a descendu, tout seul.",
            "papa|Tes bottes ont de la farine, au bord.",
            "narrateur|Le fournil garde sa chaleur ronde.",
        ],
        (1, 2, 3): [
            f"narrateur|{obj.capitalize()} est taché de tomate, un côté.",
            "narrateur|Le chien a une patte rouge, lui aussi.",
            f"{CHILD}|On a écrasé la même tomate.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Le coq sous la grille, puis dehors.",
            "maman|Tes bottes ont fini hors du rang.",
            "narrateur|Une tomate fendue brille, oubliée.",
        ],
        (1, 3, 1): [
            f"narrateur|{obj.capitalize()} porte une plume, collée au caoutchouc.",
            "narrateur|La poule picore au seuil, calme.",
            f"{CHILD}|Elle est entrée la première, pas moi.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Le coq qui a piqué l'air, puis arrêté.",
            "papa|Tes bottes ont une paille, et une plume.",
            "narrateur|Le loquet bleu ne tape plus.",
        ],
        (1, 3, 2): [
            f"narrateur|{obj.capitalize()} a de la farine, et une plume.",
            "narrateur|La poule picore la pierre, sans bruit.",
            f"{CHILD}|Mes mains ont fait trop de nuage.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Quand le coq a baissé l'aile.",
            "maman|Tes bottes ont tiédi, près du four.",
            "narrateur|La vapeur du pain rejoint le lait.",
        ],
        (1, 3, 3): [
            f"narrateur|{obj.capitalize()} sent la tomate, et la plume.",
            "narrateur|La poule reste au bout du rang.",
            f"{CHILD}|Ma paume était trop rouge, trop vite.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Les mains vides, et lui qui est venu.",
            "papa|Tes bottes ont de la terre, au talon.",
            "narrateur|Les feuilles bougent, puis s'arrêtent.",
        ],
        (2, 1, 1): [
            f"narrateur|{obj.capitalize()} sonne, presque vide, contre le bois.",
            "narrateur|Le chat se recouche dans la paille.",
            f"{CHILD}|Deux grains, et le coq est venu.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|La paille dans son poil, comme ma botte.",
            "maman|Tes bottes ont ramené le chemin, collé.",
            "narrateur|Le volet bleu tape, une dernière fois.",
        ],
        (2, 1, 2): [
            f"narrateur|{obj.capitalize()} a un fond de farine, collant.",
            "narrateur|Le chat éternue, plus loin, sous la table.",
            f"{CHILD}|Le dernier grain a suffi.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|La pierre tiède, et lui qui descend.",
            "papa|Tes bottes ont un croissant de farine.",
            "narrateur|Le pain dore, et le lait attend.",
        ],
        (2, 1, 3): [
            f"narrateur|{obj.capitalize()} porte un grain rouge.",
            "narrateur|Le chat se frotte à un tuteur.",
            f"{CHILD}|Le rang était trop étroit, pour courir.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Les deux grains, et le bec prudent.",
            "maman|Tes bottes ont de la boue, et du jus.",
            "narrateur|La grille cliquette, puis se tait.",
        ],
        (2, 2, 1): [
            f"narrateur|{obj.capitalize()} sonne plus léger, vidé d'eau.",
            "narrateur|Le chien s'allonge, nez vers le loquet.",
            f"{CHILD}|Il a bu, puis il a senti le toc.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Quand il s'est assis, trop large, puis plus.",
            "papa|Tes bottes ont tenu, malgré la flaque.",
            "narrateur|Le cabanon garde son silence rond.",
        ],
        (2, 2, 2): [
            f"narrateur|{obj.capitalize()} sent le pain, un peu vide.",
            "narrateur|Le chien rêve, queue enfin calme.",
            f"{CHILD}|Le clang a tout arrêté, un moment.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Le grain sur la pierre, et lui.",
            "maman|Tes bottes ont de la farine, aux lacets.",
            "narrateur|Une casserole repose, ronde, contre le mur.",
        ],
        (2, 2, 3): [
            f"narrateur|{obj.capitalize()} a un grain collé, rouge.",
            "narrateur|Le chien lèche sa patte, dehors.",
            f"{CHILD}|Sa patte était trop lourde, dans le rang.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Le coq sous la grille, puis le grain.",
            "papa|Tes bottes ont fini propres, hors des plants.",
            "narrateur|Une tomate fendue brille, sans plus.",
        ],
        (2, 3, 1): [
            f"narrateur|{obj.capitalize()} a perdu du grain.",
            "narrateur|La poule picore le seuil, contente.",
            f"{CHILD}|Elle a sauté dedans, trop tôt.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|La ligne de grains, jusqu'au loquet.",
            "maman|Tes bottes ont une paille, coincée.",
            "narrateur|Le toc du loquet rejoint le volet.",
        ],
        (2, 3, 2): [
            f"narrateur|{obj.capitalize()} sonne, vide, près de la pierre.",
            "narrateur|La poule a de la farine au bec.",
            f"{CHILD}|Mes mains ont trop tapé, au début.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Le dernier grain, et l'aile baissée.",
            "papa|Tes bottes ont tiédi, contre le four.",
            "narrateur|La vapeur du pain touche le bol, loin.",
        ],
        (2, 3, 3): [
            f"narrateur|{obj.capitalize()} sent la feuille, et le grain.",
            "narrateur|La poule picore une fente, sans nous.",
            f"{CHILD}|La ligne de grains l'a menée, puis lui.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Les mains vides, et le rang calme.",
            "maman|Tes bottes ont de la terre, rien de rouge.",
            "narrateur|Les tomates luisent, et le coq picore.",
        ],
        (3, 1, 1): [
            f"narrateur|{obj.capitalize()} porte une paille, et un poil.",
            "narrateur|Le chat se recouche, loin du tissu.",
            f"{CHILD}|Il a cru que c'était un lit.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|La paille sur lui, comme sur ma botte.",
            "papa|Tes bottes ont fait le chemin, sans geler.",
            "narrateur|Le volet bleu tape, et le loquet aussi.",
        ],
        (3, 1, 2): [
            f"narrateur|{obj.capitalize()} a de la farine, au coin.",
            "narrateur|Le chat se lèche, sous la table tiède.",
            f"{CHILD}|Le doudou a servi de pierre, presque.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Quand je l'ai posé, et lui est venu.",
            "maman|Tes bottes sentent le pain, un peu.",
            "narrateur|Le lait fume moins, dans la maison.",
        ],
        (3, 1, 3): [
            f"narrateur|{obj.capitalize()} a une tache de feuille, verte.",
            "narrateur|Le chat s'assoit hors du rang, sage.",
            f"{CHILD}|Il a chassé, puis il a regardé.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Le doudou au bout, et le coq.",
            "papa|Tes bottes ont de la boue, au talon.",
            "narrateur|La grille des tomates reste ouverte.",
        ],
        (3, 2, 1): [
            f"narrateur|{obj.capitalize()} a une trace de boue, allongée.",
            "narrateur|Le chien pose le museau, sans tirer.",
            f"{CHILD}|Il a cru que c'était une corde.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Quand j'ai ouvert la main, et le toc.",
            "maman|Tes bottes ont tenu, malgré le jeu.",
            "narrateur|Le cabanon redevient un secret, sombre.",
        ],
        (3, 2, 2): [
            f"narrateur|{obj.capitalize()} sent le pain, et le poil.",
            "narrateur|Le chien s'allonge, loin de la casserole.",
            f"{CHILD}|Sa queue a failli tout casser.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Le doudou sur la pierre, et lui.",
            "papa|Tes bottes ont de la farine, au bord.",
            "narrateur|Le fournil souffle, plus bas, plus calme.",
        ],
        (3, 2, 3): [
            f"narrateur|{obj.capitalize()} a un point rouge, minuscule.",
            "narrateur|Le chien s'assoit hors des plants, enfin.",
            f"{CHILD}|Sa patte était trop lourde, pour les fruits.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|Le coq sous la grille, puis vers nous.",
            "maman|Tes bottes ont fini hors de la terre rouge.",
            "narrateur|Une tomate fendue brille, et s'arrête.",
        ],
        (3, 3, 1): [
            f"narrateur|{obj.capitalize()} porte une plume, comme un nid.",
            "narrateur|La poule picore au seuil, sans s'asseoir.",
            f"{CHILD}|Elle a voulu un nid, trop tôt.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Le loquet, et le coq d'un pas.",
            "papa|Tes bottes ont une paille, obstinée.",
            "narrateur|Le toc du volet rejoint le bois.",
        ],
        (3, 3, 2): [
            f"narrateur|{obj.capitalize()} a de la farine, en nid.",
            "narrateur|La poule picore, loin des mains.",
            f"{CHILD}|J'ai trop tapé, au début.",
            "papa|Quel moment tu gardes ?",
            f"{CHILD}|La pierre tiède, et l'aile baissée.",
            "maman|Tes bottes ont pris la chaleur du four.",
            "narrateur|La vapeur du pain rejoint le lait, là-bas.",
        ],
        (3, 3, 3): [
            f"narrateur|{obj.capitalize()} sent la tomate, et la plume.",
            "narrateur|La poule picore, au bout, sans nid.",
            f"{CHILD}|Ma paume était trop pleine, trop vite.",
            "maman|Quel moment tu gardes ?",
            f"{CHILD}|Les mains vides, et lui dans le rang.",
            "papa|Tes bottes ont de la terre, rien d'autre.",
            "narrateur|Les feuilles des tomates s'arrêtent, enfin.",
        ],
    }[(a, b, c)]
    # first two lines unique to combo already; add house return
    near = {1: "du cabanon", 2: "du fournil", 3: "des tomates"}[c]
    head = [
        "narrateur|Ils reprennent le chemin de terre, lentement.",
        f"narrateur|{ani.capitalize()} reste près {near}.",
    ]
    return head + traces


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=le_toc_du_volet_a_trouvé_le_coq; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "coq,volet,lait", {"emphasis": "volet bleu"})
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "le ballon rouge",
            "option_2_label": "le seau bleu",
            "option_3_label": "le doudou",
        }},
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            OBJ[a]["sons"],
            {"emphasis": OBJ[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"night_policy": "skip", "fields": Q_FIELDS, "emphasis": "bottes"},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            "bottes,caoutchouc",
            {"emphasis": "bottes"},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "le chat",
                "option_2_label": "le chien",
                "option_3_label": "la poule",
            }},
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                ANI[b]["sons"],
                {"emphasis": ANI[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le secret du cabanon",
                    "option_2_label": "le fournil",
                    "option_3_label": "les tomates",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    LIEU[c]["sons"],
                    {"emphasis": "coq"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "bottes,lait",
                    {"emphasis": "bottes", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = [out_chunks[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    t3_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"]
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
        "Après la pluie, à la ferme, le volet bleu tape toc. Le coq a chanté "
        "une fois derrière la grange, puis s'est tu. Raphaël veut le rejoindre "
        "tout de suite, ballon, seau de grain ou doudou à la main. Pieds nus, "
        "la pierre mouillée le pique : il met la botte gauche, puis la droite. "
        "Sur le chemin, chat, chien ou poule font autre chose que prévu. "
        "La première idée rate. L'animal montre trois coins : le secret du "
        "cabanon, le fournil, les tomates. Raphaël comprend sans forcer le coq. "
        "Le toc du loquet paie le volet. Les bottes gardent boue et paille."
    )
    merged["title"] = TITLE
    merged["characters"] = "Raphaël, papa, maman"
    merged["setting"] = "ferme, volet bleu, paille, grange, chemin de terre mouillé"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    if min(counts) < 380:
        raise SystemExit(f"chemin trop court: min {min(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rel = ROOT / SID / "RELECTURE.md"
    rel.write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019. Graphe, `chunk_id`, types de blocs "
        "et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Après la pluie, le volet bleu de la ferme tape toc. Le coq a chanté "
        "une fois derrière la grange, puis s'est tu. Raphaël veut le rejoindre "
        "maintenant, avec un ballon rouge, un seau bleu de grain ou son doudou. "
        "Le chemin de terre est mouillé : les chaussons échouent, les bottes "
        "passent, gauche puis droite. Chat, chien ou poule font quelque chose "
        "d'inattendu. La première idée rate. L'animal montre trois coins nommés "
        "dans la ferme : le secret du cabanon, le fournil, les tomates. Raphaël "
        "comprend sans forcer le coq. Le toc du loquet paie le volet du début. "
        "Les bottes gardent boue et paille.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : ferme, volet bleu, paille, grange, chemin de terre mouillé.\n"
        "- Désir : rejoindre le coq avant qu'il se cache.\n"
        "- Objet : ballon / seau de grain / doudou, plus les bottes (équipement).\n"
        "- Urgence douce : le chant s'est arrêté.\n"
        "- Imprévu 1 : sortir pieds nus, objet qui glisse, pierre froide.\n"
        "- Cue : botte gauche, puis droite. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : l'animal ne se laisse pas faire ; il montre.\n"
        "- Résolution : attendre, poser l'objet, ne pas forcer le coq.\n"
        "- Retour : toc, paille, boue, objet marqué, 27 souvenirs distincts.\n\n"
        "## Corrections éditoriales\n\n"
        "- Le premier choix n'enlève pas les bottes : objet compagnon, puis bottes.\n"
        "- T3 n'est plus un simple moment de la journée : cabanon / fournil / tomates.\n"
        "- Neuf obstacles animaux distincts, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.ROU.001 vécue (gauche puis droite, puis le chemin), jamais dite.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Troupe D16 : Raphaël, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience au départ, petit découragement quand l'objet ou l'animal résiste, "
        "fierté calme quand Raphaël agit seul. L'adulte guide peu. `slow` réservé "
        "aux choix, à la question, à l'émotion du retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N1 ≤ 10 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
