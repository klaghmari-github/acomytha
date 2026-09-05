#!/usr/bin/env python3
"""TREE-COL-007 — La porte embuée et les bottes de Nino (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-007"
N2 = LIMITS["N2"]
TITLE = "La porte embuée et les bottes de Nino"
FIL = (
    "La paume de papa chauffe la poignée : la porte vitrée s'embue. "
    "Un croissant de buée s'y dessine, à hauteur des bottes vertes de Nino. "
    "Il veut les poser au radiateur et ramener le bonnet de Sarah avant que "
    "la buée sèche. Il parle trop tôt : on n'entend que « lourdes ». "
    "Tapis, table ou préau changent l'obstacle. Histoire, dessin ou chanson "
    "changent la deuxième ruse. Maman, papa ou Sarah changent l'oreille du soir. "
    "Le croissant de buée paie la fin, sur les bottes devenues légères."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="croissant de buée",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=la_phrase_va_se_perdre_dans_la_buee; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=sa_phrase_attend_le_soir; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_phrase_a_trouve_un_creux; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="bottes",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=couper_fait_rater_l_oreille; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=attendre_a_ouvert_l_oreille; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="bottes",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_croissant_a_rendu_la_phrase; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        parts = re.findall(r".+?[.!?]", ph.strip())
        leftover = ph.strip()
        for p in parts:
            leftover = leftover.replace(p, "", 1)
        if leftover.strip():
            raise SystemExit(f"reste {leftover!r}: {ph}")
        if not parts:
            raise SystemExit(f"sans phrase: {ph}")
        for part in parts:
            part = part.strip()
            n = words(part)
            if n > N2:
                raise SystemExit(f"{n}>{N2}: {part}")
            if TICS.search(part):
                raise SystemExit(f"tic: {part}")
            if role == "narrateur":
                tok = part.split()[0].lower()
                run = run + 1 if tok == prev else 1
                prev = tok
                if run >= 4:
                    raise SystemExit(f"puces {tok}: {part}")
            else:
                prev = ""
                run = 1
            out.append(f"{role}|{part}")
    return out


def ssml(text: str, m: dict) -> str:
    body = html.escape(text, quote=False)
    emp = m.get("emphasis")
    if emp and emp in text:
        e = html.escape(emp, quote=False)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
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
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(nc: dict, profile: str, extra_note: str = "", emphasis: str | None | bool = False) -> None:
    m = dict(PROFILES[profile])
    if emphasis is not False:
        m["emphasis"] = emphasis
    text = nc["text"]
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
    nc["pause_before_ms"] = 0
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
    note = m["note"]
    if extra_note:
        note = note + "; " + extra_note
    nc["notes"] = note
    nc["night_policy"] = nc.get("night_policy") or "play"
    nc["locale"] = nc.get("locale") or "fr-FR"
    nc["voice_id"] = nc.get("voice_id") or "fr_FR-siwis-medium"


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str, ok: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
        "engine_ok_text": ok,
        "engine_near_text": "Tu es proche. Écoute l'indice.",
    }


def profile_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "opening"
    if kind == "transition_question":
        return "choice"
    if kind == "passage_question":
        return "clue"
    if kind == "passage_fin":
        return "ending"
    if cid.endswith("_C0001"):
        return "confirm"
    if "_T0003_P000" in cid and cid[-1] in "123":
        return "resolution"
    if "_T0002_P000" in cid and cid[-1] in "123":
        return "obstacle"
    return "action"


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

DEBUT = L(
    "narrateur|La main de papa pose une paume chaude sur la poignée.",
    "narrateur|La porte vitrée de l'école s'embue sous leur souffle.",
    "narrateur|Un croissant de buée s'y dessine, à hauteur de bottes.",
    "narrateur|Dehors, une flaque ronde tient un morceau de ciel.",
    "narrateur|Un moineau secoue ses plumes, très vite.",
    "narrateur|Ça sent la laine mouillée, dans le hall des gouttes.",
    "narrateur|Le radiateur fait tic, tic, contre le fer.",
    "maman|Tes bottes, Nino.",
    "maman|Elles gouttent sur les carreaux.",
    "enfant-m|Elles sont lourdes.",
    "papa|On les pose près du radiateur ?",
    "enfant-m|Oui, avant qu'elles restent mouillées !",
    "narrateur|Nino parle pendant que maman parle du bonnet.",
    "narrateur|Deux voix se marchent dessus, près du verre.",
    "papa|Tu disais lourdes, Nino ?",
    "enfant-m|Les bottes, et le bonnet de Sarah !",
    "narrateur|Le croissant de buée avale la fin de la phrase.",
    "narrateur|Deux virgules sombres restent au sol, sous les boucles.",
    "narrateur|Un bonnet rouge attend sur le banc.",
    "maman|Sarah l'a oublié, ce matin.",
    "enfant-m|Il est humide, comme mes bottes.",
    "papa|On le ramène ce soir.",
    "narrateur|En ce moment, Nino accroche son manteau.",
    "enfant-m|J'avais autre chose à dire.",
    "maman|On t'écoute ce soir, d'accord ?",
    "enfant-m|D'accord.",
    "narrateur|Le moineau a disparu.",
    "narrateur|La flaque reste.",
)

T1Q = L(
    "narrateur|Nino peut s'asseoir à trois endroits.",
    "papa|Le tapis, la table, ou le préau ?",
    "maman|Où poses-tu les genoux, cette fois ?",
)

T1 = {
    1: L(
        "narrateur|Nino pose les genoux sur le tapis rêche.",
        "narrateur|Les carrés sont bleus et gris, un peu rudes.",
        "narrateur|Ça sent la poussière et le savon.",
        "enfant-m|Ma phrase, je la dis maintenant !",
        "narrateur|Un camarade chuchote près de l'oreille.",
        "narrateur|Les mots de Nino se cognent au chuchotis.",
        "narrateur|Personne ne se tourne. Le tapis avale tout.",
        "narrateur|Le sourire de Nino disparaît.",
        "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
        "narrateur|Il rentre la phrase, les épaules hautes.",
        "narrateur|Il attend que le chuchotis se taise.",
        "papa|Je m'accroupis, à la hauteur des bottes.",
        "maman|J'ai fini, près de la porte.",
        "maman|Je t'écoute.",
        "enfant-m|Un camarade a parlé trop près.",
        "enfant-m|Ça m'a serré le ventre.",
        "papa|Merci d'avoir attendu le silence.",
        "narrateur|Une fibre bleue brille, sous une goutte de lumière.",
    ),
    2: L(
        "narrateur|Nino grimpe sur la chaise, près de la table.",
        "narrateur|Le bois est lisse, un peu froid.",
        "enfant-m|Ma phrase, tout de suite !",
        "narrateur|La chaise racle. Le bruit couvre les mots.",
        "narrateur|La maîtresse lève les yeux, puis reprend.",
        "narrateur|Nino se rassoit, le ventre serré.",
        "narrateur|Le sourire de Nino disparaît.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Il pose les mains à plat, sur le bois.",
        "narrateur|Il attend que la racle se taise.",
        "papa|Je m'accroupis, près des pieds de la chaise.",
        "maman|Ta phrase, on la prend dans le calme ?",
        "enfant-m|Oui. Un camarade a parlé trop fort.",
        "enfant-m|Ça m'a pincé, ici.",
        "papa|Merci d'avoir gardé tes mains sur la table.",
        "narrateur|Un crayon roule, et s'arrête contre sa manche.",
    ),
    3: L(
        "narrateur|La classe sort sous le préau de bois.",
        "narrateur|Une goutte tombe du toit, ploc.",
        "enfant-m|Ma phrase, je la crie dehors !",
        "narrateur|Le ploc avale les mots, un par un.",
        "narrateur|Nino ouvre la bouche, puis la referme.",
        "narrateur|Le sourire de Nino disparaît.",
        "narrateur|Dans sa poitrine, l'élan et la peur se bousculent.",
        "narrateur|Il compte les gouttes, un, deux, trois.",
        "narrateur|Un creux arrive, sans ploc.",
        "papa|Je m'accroupis, à la hauteur des boucles.",
        "maman|Tu cherches un silence, entre les gouttes ?",
        "enfant-m|Oui. Ma voix n'a pas passé.",
        "enfant-m|Le ventre s'est serré.",
        "papa|Merci d'avoir attendu le creux.",
        "narrateur|La goutte dessine un point sur le bois mouillé.",
    ),
}

Q1 = {
    1: L(
        "narrateur|Le ventre de Nino s'est serré, sur le tapis.",
        "maman|Que veut-il faire, ce soir ?",
    ),
    2: L(
        "narrateur|Sa phrase s'est perdue, près de la table.",
        "papa|Que veut-il faire, plus tard ?",
    ),
    3: L(
        "narrateur|Les gouttes ont couvert sa voix, au préau.",
        "maman|Que veut-il faire, à la maison ?",
    ),
}

C1 = {
    1: L(
        "enfant-m|Raconter.",
        "papa|Oui, raconter.",
        "maman|Merci. J'ai eu toute la phrase.",
        "narrateur|Les bottes sèchent, près du tic.",
        "narrateur|Le bonnet rouge attend sur le banc.",
        "enfant-m|Je garde ma phrase pour ce soir.",
        "papa|Qui t'écoutera, à la maison ?",
    ),
    2: L(
        "enfant-m|Raconter.",
        "maman|Oui.",
        "papa|Merci d'avoir posé les mains.",
        "narrateur|Les bottes restent près du radiateur.",
        "narrateur|Le crayon dort contre la manche.",
        "enfant-m|Ma phrase tient, dans la poitrine.",
        "maman|Qui t'écoutera, ce soir ?",
    ),
    3: L(
        "enfant-m|Raconter.",
        "papa|Oui, ce soir.",
        "maman|Merci d'avoir compté les gouttes.",
        "narrateur|Les bottes claquent un peu, sous le préau.",
        "narrateur|Le bonnet rouge reste au sec, dans le hall.",
        "enfant-m|Je dis ma phrase à la maison.",
        "papa|Qui aura tes mots, plus tard ?",
    ),
}

T2Q = {
    1: L(
        "narrateur|Sur le tapis, trois jeux attendent la phrase.",
        "maman|L'histoire, le dessin, ou la chanson ?",
        "papa|Qu'est-ce qui la garde, maintenant ?",
    ),
    2: L(
        "narrateur|À la table, trois jeux peuvent aider les mots.",
        "papa|L'histoire, le dessin, ou la chanson ?",
        "maman|Lequel prend ta phrase, sans la casser ?",
    ),
    3: L(
        "narrateur|Sous le préau, trois jeux gardent le silence.",
        "maman|L'histoire, le dessin, ou la chanson ?",
        "papa|Où poses-tu ta phrase, entre les gouttes ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Sur le tapis, la maîtresse ouvre un livre.",
        "narrateur|La couverture est jaune, un peu usée.",
        "narrateur|Nino pose les mains à plat, sur la laine.",
        "enfant-m|Ce mot, il pince !",
        "narrateur|Sa voix coupe la page, au milieu.",
        "narrateur|La maîtresse s'arrête. Le livre tremble.",
        "narrateur|Nino rentre le mot, les joues chaudes.",
        "maitresse|J'arrive au point. Ensuite, c'est toi.",
        "narrateur|Il écoute jusqu'au point, sans bouger.",
        "narrateur|Sur la vitre, le croissant de buée pâlit.",
        "enfant-m|Le mot pince. Je le garde.",
        "papa|Plus tard, la porte s'ouvre.",
    ),
    (1, 2): L(
        "narrateur|Sur le tapis, une feuille arrive, blanche.",
        "narrateur|Nino veut le crayon jaune, pour les bottes.",
        "narrateur|Un camarade le prend au même instant.",
        "enfant-m|C'est pour mes bottes !",
        "narrateur|Deux mains tirent. Le bois craque, presque.",
        "narrateur|Il lâche, les doigts vides, le ventre dur.",
        "maitresse|Un crayon après l'autre. Ensuite, c'est toi.",
        "narrateur|Nino attend. Une fibre bleue brille.",
        "narrateur|Quand le jaune revient, il trace deux virgules.",
        "narrateur|Sur la vitre, le croissant de buée revient.",
        "enfant-m|Mes bottes, en dessin.",
        "maman|On voit les boucles, et on voit l'attente.",
    ),
    (1, 3): L(
        "narrateur|Sur le tapis, une chanson commence, toute basse.",
        "enfant-m|Le refrain, c'est moi !",
        "narrateur|Sa voix part trop tôt. Le fil se casse.",
        "narrateur|Les autres s'arrêtent. Nino pince les lèvres.",
        "maitresse|On reprend. Toi, tu prends le trou.",
        "narrateur|Il attend le silence entre deux couplets.",
        "narrateur|Cette fois, sa note a toute la laine.",
        "narrateur|Le croissant de buée tremble, puis tient.",
        "enfant-m|J'ai trop chanté tôt. Après, on m'a entendu.",
        "papa|La porte s'ouvre, sur le dernier mot.",
        "narrateur|Une fibre du tapis vibre, comme un tambour.",
    ),
    (2, 1): L(
        "narrateur|À la table, le livre s'ouvre contre le carton.",
        "narrateur|La page sent l'encre, un peu sèche.",
        "enfant-m|C'est mon mot à moi !",
        "narrateur|Sa phrase recouvre celle de la maîtresse.",
        "narrateur|Deux voix se marchent dessus. Le livre se ferme.",
        "narrateur|Nino mord sa lèvre, déçu.",
        "maitresse|Je recommence la dernière phrase.",
        "narrateur|Cette fois, Nino laisse la voix aller au point.",
        "narrateur|Sur la vitre, le croissant de buée s'affine.",
        "enfant-m|Le mien pince. Le sien est lisse.",
        "papa|Le crayon, sur la table, ne roule plus.",
        "maman|Plus tard, on t'écoute jusqu'au bout.",
    ),
    (2, 2): L(
        "narrateur|À la table, Nino aligne feuille et crayon.",
        "narrateur|Il veut tracer les bottes, tout de suite.",
        "narrateur|Un pot de colle penche vers le papier.",
        "enfant-m|Mon dessin !",
        "narrateur|Le cri coupe la consigne. La colle saute.",
        "narrateur|Un nuage blanc cache le jaune.",
        "maitresse|On souffle d'abord. Ensuite, tu traces.",
        "narrateur|Nino attend que le nuage retombe.",
        "narrateur|Il dessine deux virgules, sans colle.",
        "narrateur|Le croissant de buée guide le regard vers le trait.",
        "papa|On voit les bottes, et on voit le calme.",
        "enfant-m|Sans le pot, le papier reste net.",
    ),
    (2, 3): L(
        "narrateur|À la table, on tapote le bois, pour le rythme.",
        "enfant-m|C'est ma chanson de table !",
        "narrateur|Deux rythmes se battent. La chaise tressaute.",
        "maitresse|Un tap, puis l'autre. Le tien après le mien.",
        "narrateur|Nino compte, les mains sur le bois froid.",
        "narrateur|Il glisse sa note dans le trou.",
        "narrateur|Le croissant de buée s'arrondit, sur la vitre.",
        "enfant-m|J'ai trop serré le couplet. Après, j'ai eu le trou.",
        "papa|La racle s'est tue. Ta note reste.",
        "maman|Le soir, on te prend ce trou-là.",
        "narrateur|Le crayon dort, sans rouler.",
    ),
    (3, 1): L(
        "narrateur|Sous le préau, la maîtresse tient le livre ouvert.",
        "narrateur|Le vent tourne une page, trop vite.",
        "enfant-m|Le mot du livre, il part !",
        "narrateur|Son cri coupe le mot. Une goutte tombe.",
        "narrateur|La page se tache, juste sur un rond.",
        "narrateur|Nino se tait, les épaules basses.",
        "maitresse|On écoute la fin, malgré le vent.",
        "narrateur|Il laisse la phrase aller au point.",
        "narrateur|Le croissant de buée réapparaît, sur une vitre.",
        "enfant-m|Le mot a eu son abri. Moi, une goutte.",
        "maman|Tu as laissé la page aller au bout.",
        "narrateur|Le point d'eau sèche au bord du livre.",
    ),
    (3, 2): L(
        "narrateur|Sous le préau, Nino pose une feuille sur le bois.",
        "narrateur|Un crayon jaune glisse vers une flaque.",
        "enfant-m|La goutte !",
        "narrateur|Il parle pile, pour le crayon.",
        "narrateur|Personne ne gronde. Le bois est sauvé.",
        "maitresse|Merci. Ensuite, on dessine.",
        "narrateur|Nino trace un ploc, puis deux virgules de bottes.",
        "narrateur|Le croissant de buée montre le trait, tout net.",
        "enfant-m|J'ai parlé pour le crayon. Après, j'ai attendu.",
        "papa|Tu as parlé pile. Puis tu as tracé.",
        "narrateur|La feuille reste sèche, loin du ploc.",
    ),
    (3, 3): L(
        "narrateur|Sous le préau, une chanson part entre les gouttes.",
        "enfant-m|Soleil, soleil !",
        "narrateur|Le ploc recouvre la note. Rien n'est clair.",
        "narrateur|Nino pince les lèvres, les joues froides.",
        "maitresse|On chante dans le creux, pas dans l'eau.",
        "narrateur|Il compte un, deux, trois, puis glisse sa note.",
        "narrateur|Le croissant de buée tient, malgré le vent.",
        "enfant-m|Ma note a eu le silence, cette fois.",
        "papa|Plus tard, la porte s'ouvre, sans ploc.",
        "maman|On t'écoute, dans un vrai creux.",
        "narrateur|Une goutte sèche sur le bois, un point pâle.",
    ),
}

T3Q = {
    1: L(
        "narrateur|Le soir, Nino raconte à quelqu'un.",
        "maman|Maman, papa, ou Sarah ?",
        "papa|Qui aura toute la phrase ?",
    ),
    2: L(
        "narrateur|Le soir, la phrase cherche une oreille.",
        "papa|Maman, papa, ou Sarah ?",
        "maman|À qui la donnes-tu, sans la casser ?",
    ),
    3: L(
        "narrateur|Le soir, le bonnet rouge rentre, un peu humide.",
        "maman|Maman, papa, ou Sarah ?",
        "papa|Qui t'écoute jusqu'au bout, cette fois ?",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Le soir, la maison sent la soupe.",
        "narrateur|La lampe fait un rond jaune, sur la casserole.",
        "narrateur|Nino rejoint maman, les bottes à la main.",
        "enfant-m|Maman, le mot du livre !",
        "narrateur|La cuillère tourne. Les mots se perdent dans la vapeur.",
        "narrateur|Nino ferme la bouche. Ça a failli rater.",
        "narrateur|Il attend que la cuillère se pose.",
        "narrateur|Sur la vitre, un croissant de buée revient.",
        "enfant-m|Un camarade a chuchoté. Un mot a pincé.",
        "maman|Je t'écoute, là.",
        "papa|Toute la phrase, cette fois.",
        "narrateur|Les bottes posent deux virgules sèches, près du four.",
    ),
    (1, 1, 2): L(
        "narrateur|Le soir, papa verse le cacao, le dos un peu tourné.",
        "enfant-m|Papa, le mot du tapis !",
        "narrateur|Le filet de cacao couvre la moitié des mots.",
        "narrateur|Nino s'assoit. Il refuse de jeter la phrase.",
        "narrateur|Il attend que la tasse se remplisse.",
        "papa|Me voilà. Le mot, le tapis, les bottes.",
        "enfant-m|J'ai coupé le livre. Après, j'ai attendu le point.",
        "maman|On a toute la phrase, dans la tasse.",
        "narrateur|Un croissant de vapeur imite celui de la porte.",
        "narrateur|Les boucles vertes font clic, près du bois.",
        "enfant-m|Mes bottes sont légères, maintenant.",
    ),
    (1, 1, 3): L(
        "narrateur|Le soir, Sarah tient son bol, près du bonnet rouge.",
        "enfant-m|Sarah, le mot du livre !",
        "narrateur|Elle mâche. Les mots se cognent aux miettes.",
        "narrateur|Nino attend que sa bouche soit libre.",
        "enfant-f|Je t'écoute, Nino.",
        "enfant-m|Un camarade a chuchoté. Le mot a pincé.",
        "enfant-f|Tu as gardé ta phrase. Moi, le bonnet.",
        "maman|On a deux oreilles, ici.",
        "papa|Les bottes sèchent, près du bol.",
        "narrateur|Sarah touche le bonnet, du bout du doigt.",
        "narrateur|Un croissant de buée s'arrondit sur la cuillère.",
    ),
    (1, 2, 1): L(
        "narrateur|Le soir, un peu de jaune reste au doigt de Nino.",
        "narrateur|La soupe fume. Maman essuie la nappe.",
        "enfant-m|Maman, le crayon, les virgules, le tapis !",
        "narrateur|Le doigt jaune manque de tâcher la nappe.",
        "maman|D'abord tes mots. Après, on essuie.",
        "narrateur|Nino attend que la phrase de maman finisse.",
        "enfant-m|J'ai attendu le crayon. J'ai tracé deux virgules.",
        "narrateur|Maman souffle sur le doigt, puis sur le papier.",
        "narrateur|Le croissant de buée semble s'y poser.",
        "papa|On le met près des bottes, maintenant ?",
        "enfant-m|Oui. Sans colle, juste le trait.",
    ),
    (1, 2, 2): L(
        "narrateur|Le soir, le crayon de poche dépasse du manteau.",
        "narrateur|Papa range les chaussures, le dos tourné.",
        "enfant-m|Regarde mes virgules !",
        "narrateur|Papa entend le mot virgules, pas le reste.",
        "narrateur|Nino s'assoit, le crayon en l'air.",
        "narrateur|Il attend qu'il se tourne.",
        "papa|Je te vois. Montre-moi.",
        "enfant-m|À l'école, j'ai tracé les bottes, après l'attente.",
        "narrateur|Papa pose le crayon à côté, sans le prendre.",
        "maman|Le rond de la lampe est assez grand pour deux.",
        "narrateur|Les bottes et le crayon dorment dans la lumière.",
    ),
    (1, 2, 3): L(
        "narrateur|Le soir, Sarah a un point jaune au bout du nez.",
        "narrateur|Nino l'a serrée avec le doigt marqué de jaune.",
        "enfant-m|Pardon. C'est le dessin du tapis.",
        "narrateur|Il veut tout dire d'un coup. Le bol bascule.",
        "narrateur|Il le rattrape, et il recommence, plus bas.",
        "enfant-m|J'ai attendu le crayon. J'ai dessiné les boucles.",
        "enfant-f|Je t'écoute, Nino.",
        "papa|On t'écoute, nous aussi.",
        "maman|Le point jaune, c'est une trace du jour.",
        "narrateur|Sarah pose le bonnet près des bottes sèches.",
        "narrateur|Un croissant pâle reste sur le bois du bol.",
    ),
    (1, 3, 1): L(
        "narrateur|Le soir, Nino entre en chantant le couplet des bottes.",
        "narrateur|La louche de maman tape à côté, pas ensemble.",
        "enfant-m|C'est ma chanson !",
        "maman|La mienne, c'est la soupe. Une après l'autre.",
        "narrateur|Nino se tait, les bottes contre la poitrine.",
        "narrateur|La louche finit son toc. La cuisine s'ouvre.",
        "enfant-m|Sur le tapis, j'ai chanté trop tôt. Après, on m'a entendu.",
        "maman|Chante-moi le trou, maintenant.",
        "narrateur|Nino pose les bottes, et glisse sa note.",
        "papa|Le croissant de buée suit le rythme, tout bas.",
        "narrateur|La soupe fume, sans recouvrir la chanson.",
    ),
    (1, 3, 2): L(
        "narrateur|Le soir, papa chante en rangeant le manteau.",
        "enfant-m|Bottes, bottes !",
        "narrateur|Les deux voix se marchent dessus, près du tapis.",
        "papa|Laisse-moi finir. Ensuite, ton couplet.",
        "narrateur|Nino attend, un pied sur la laine.",
        "enfant-m|À l'école, j'ai trop chanté tôt. Le fil a cassé.",
        "narrateur|Papa s'arrête pile, et penche l'oreille.",
        "enfant-m|Bottes, bottes, sur le tapis.",
        "maman|Cette fois, ta note a toute la place.",
        "narrateur|Les boucles vibrent, comme un petit tambour.",
        "papa|On les pose près du radiateur, sur le dernier mot.",
    ),
    (1, 3, 3): L(
        "narrateur|Le soir, Nino pose le bonnet de Sarah sur le tapis.",
        "enfant-m|Toi, tu écoutes la chanson. Après, les mots.",
        "narrateur|Il commence trop fort. Le bonnet bascule.",
        "narrateur|Il le redresse, et reprend plus bas.",
        "enfant-m|Bottes mouillées, non. Bottes du tapis.",
        "enfant-f|On a le droit d'écouter, nous aussi ?",
        "enfant-m|Oui. Le trou, c'est pour vous.",
        "papa|On le prend, ce trou.",
        "maman|Le bonnet s'arrête dans la lumière.",
        "narrateur|Les bottes s'y installent, enfin légères.",
        "narrateur|Un croissant de buée s'endort sur la vitre.",
    ),
    (2, 1, 1): L(
        "narrateur|Le soir, l'assiette ronde attend près de la soupe.",
        "narrateur|Nino pose une botte contre le bord, trop vite.",
        "enfant-m|C'est le mot du livre, maman !",
        "narrateur|Une goutte de soupe manque le cuir vert.",
        "maman|L'assiette d'abord. Tes mots, juste après.",
        "narrateur|Nino recule la botte, les épaules hautes, puis basses.",
        "enfant-m|À la table, j'ai coupé l'histoire. Le livre s'est fermé.",
        "enfant-m|Après, j'ai attendu le point.",
        "maman|Là, j'ai tout. Merci.",
        "narrateur|Il lisse la botte loin de la vapeur.",
        "papa|Le croissant de la vitre a de la place, pour lui.",
    ),
    (2, 1, 2): L(
        "narrateur|Le soir, papa ouvre un vrai livre, dans le fauteuil.",
        "enfant-m|Le mien, à la table, s'était fermé !",
        "narrateur|Sa phrase recouvre la sienne. La page claque.",
        "papa|Je finis celle-ci. Puis c'est la tienne.",
        "narrateur|Nino s'assoit par terre, une botte sur les genoux.",
        "enfant-m|Le mot d'école a pincé. J'ai attendu le point.",
        "papa|Je vois les deux, maintenant.",
        "maman|On t'écoute jusqu'à ton point.",
        "narrateur|Papa glisse la botte dans le rond de la lampe.",
        "enfant-m|Cette page-là, elle reste ouverte.",
        "narrateur|Un croissant de cacao imite celui de la porte.",
    ),
    (2, 1, 3): L(
        "narrateur|Le soir, Nino installe Sarah à table, face à l'assiette.",
        "enfant-m|Toi, tu es la maîtresse. J'ouvre le livre.",
        "narrateur|Il parle trop vite. Le bol glisse sur le bois.",
        "narrateur|Il le rattrape, et recommence, un mot après l'autre.",
        "enfant-m|J'ai coupé. J'ai attendu. Le mot a eu son rond.",
        "enfant-f|La maîtresse du bol a bien écouté.",
        "maman|Nous aussi, on prend notre tour.",
        "papa|Nino porte le bonnet jusqu'aux bottes.",
        "narrateur|La lampe leur fait un petit livre de lumière.",
        "narrateur|Un croissant de buée s'ouvre, puis se pose.",
        "enfant-m|Cette page-là, elle reste ouverte.",
    ),
    (2, 2, 1): L(
        "narrateur|Le soir, de la farine reste sur la table de cuisine.",
        "narrateur|Nino y pose le dessin, pour coller les virgules.",
        "enfant-m|Comme à l'école, sans le pot trop plein !",
        "narrateur|La farine saute. Un nuage blanc cache le vert.",
        "maman|On souffle d'abord. Ensuite, tu me racontes.",
        "narrateur|Nino attend que le nuage retombe.",
        "enfant-m|J'ai gardé le papier au sec, à la table.",
        "enfant-m|J'ai dessiné les boucles, tout autour.",
        "maman|Je vois le trait. Merci d'avoir attendu la farine.",
        "papa|Des bottes, un croissant, et plus de nuage.",
        "narrateur|Le dessin retrouve sa couleur, dans la lumière.",
    ),
    (2, 2, 2): L(
        "narrateur|Le soir, le bois de la table de cuisine brille.",
        "narrateur|Nino y aligne crayon et botte, comme à l'école.",
        "enfant-m|Papa, le pot allait sur mon dessin !",
        "narrateur|Papa coupe du pain, et rate la moitié des mots.",
        "narrateur|Il pose le crayon, et attend la fin de la miche.",
        "papa|Me voilà. Le pot, le papier, les virgules.",
        "enfant-m|J'ai tracé le tour des boucles, sans colle.",
        "maman|Le bois d'ici ressemble à celui de la classe.",
        "narrateur|Papa porte la botte jusqu'au radiateur, tout droit.",
        "enfant-m|Là, le croissant peut la voir.",
        "narrateur|Un trait jaune sèche au bord de la tasse.",
    ),
    (2, 2, 3): L(
        "narrateur|Le soir, Sarah reçoit le crayon, trop gros.",
        "enfant-m|Tiens, dessine les virgules.",
        "narrateur|La main n'y arrive pas. Nino rit, puis s'arrête.",
        "enfant-m|D'accord. Je raconte, tu écoutes.",
        "narrateur|Il dit le pot, la consigne, le trait jaune.",
        "enfant-f|J'ai tout gardé, Nino.",
        "papa|Nous, on a gardé une oreille, aussi.",
        "maman|Nino reprend le crayon, et pose la botte au sec.",
        "enfant-m|Toi, tu as écouté. Moi, j'ai tracé.",
        "narrateur|Un point de farine reste sur le bonnet rouge.",
        "narrateur|Le croissant de buée s'y pose, tout petit.",
    ),
    (2, 3, 1): L(
        "narrateur|Le soir, maman tapote la casserole, comme une table.",
        "enfant-m|C'est ma chanson de table !",
        "narrateur|Deux rythmes se battent. La soupe tressaute.",
        "maman|Un tap, puis l'autre. Le tien après le mien.",
        "narrateur|Nino compte, une botte contre le bois de la chaise.",
        "enfant-m|À la table, j'ai trop serré le couplet. Après, on m'a mis dans le trou.",
        "maman|Voici un trou, dans ma casserole.",
        "narrateur|Nino glisse sa note. La vapeur danse.",
        "papa|On pose les bottes quand la note est finie.",
        "narrateur|Le croissant de la vitre reçoit le vert, sans bruit.",
        "enfant-m|Cette fois, ma note a toute la place.",
    ),
    (2, 3, 2): L(
        "narrateur|Le soir, le fauteuil de papa grince en rythme.",
        "enfant-m|C'est le bois de la table, papa !",
        "narrateur|Il chante par-dessus le grincement. Rien n'est clair.",
        "papa|Je finis de m'asseoir. Ensuite, ton couplet.",
        "narrateur|Nino attend que le fauteuil se taise.",
        "enfant-m|Mes bottes sont sèches, et elles chantent bas.",
        "papa|Je les entends, cette fois.",
        "maman|La note a trouvé sa chaise.",
        "narrateur|Papa pose une botte dans le rond, au silence.",
        "enfant-m|Le bois ne tinte plus.",
        "narrateur|Un croissant de cacao s'arrondit, puis s'en va.",
    ),
    (2, 3, 3): L(
        "narrateur|Le soir, Nino fait écouter le refrain à Sarah, à table.",
        "enfant-m|Toi, tu prends le trou.",
        "narrateur|Il commence trop tôt. Le bol bascule de la chaise.",
        "narrateur|Il le rattrape, et laisse un vrai silence.",
        "enfant-m|Maintenant, c'est toi. Puis maman. Puis papa.",
        "enfant-f|On prend notre trou, avec plaisir.",
        "papa|Le silence de Sarah était le plus net.",
        "maman|Nino pose les trois : bonnet, botte, crayon.",
        "enfant-m|Chacun sa note.",
        "narrateur|Le bonnet rouge s'arrête, sec.",
        "narrateur|Un croissant de buée s'endort sur le bois.",
    ),
    (3, 1, 1): L(
        "narrateur|À la maison, une goutte sèche sur le livre rapporté.",
        "narrateur|Nino la montre à maman, au-dessus de la soupe.",
        "enfant-m|Le préau, le livre, la page tachée !",
        "narrateur|La vapeur mouille le point d'eau. Nino recule, trop tard.",
        "maman|Loin de la casserole. Je t'écoute ici.",
        "narrateur|Nino s'assoit, une botte à l'abri.",
        "enfant-m|J'ai crié trop tôt. La page s'est tachée. Après, j'ai attendu la fin.",
        "maman|Le mot a trouvé son coin sec. Toi, le nôtre.",
        "papa|On souffle sur le point. Il s'en va.",
        "narrateur|La botte, plus sèche, entre dans le rond de la lampe.",
        "narrateur|Le croissant de buée quitte la vapeur, sans un bruit.",
    ),
    (3, 1, 2): L(
        "narrateur|Le soir, papa entend un ploc, dans la voix de Nino.",
        "enfant-m|C'est le toit du préau, dans l'histoire !",
        "narrateur|Il le dit pendant qu'il ferme la porte.",
        "narrateur|Le clac recouvre le ploc. Nino pince les lèvres.",
        "papa|Recommence. La porte a fini.",
        "enfant-m|Le vent a tourné la page. Une goutte est tombée sur le mot.",
        "enfant-m|J'ai laissé la fin, malgré le vent.",
        "papa|Je tiens le ploc, maintenant.",
        "maman|Le hall d'ici n'a pas de toit. Juste un radiateur.",
        "narrateur|Nino pose les bottes. La lampe sèche le dernier point.",
        "narrateur|Un croissant de buée s'ouvre sur le verre de la porte.",
    ),
    (3, 1, 3): L(
        "narrateur|Le soir, le bonnet de Sarah a le bord froid, comme le préau.",
        "enfant-m|Toi, tu as eu le vent. Moi, la goutte.",
        "narrateur|Il parle trop vite. Le bonnet tombe du lit.",
        "narrateur|Il le réchauffe contre sa joue, puis reprend.",
        "enfant-m|Le livre a taché le rond. J'ai attendu la fin, sous le toit.",
        "enfant-f|Le bord du bonnet se réchauffe. Tes mots aussi.",
        "papa|On a de la place, près des bottes, pour un bord froid.",
        "maman|Nino les pose tous les deux dans la lumière.",
        "enfant-m|Plus de vent. Plus de goutte.",
        "narrateur|Sarah souffle sur le bonnet. Le point d'eau s'en va.",
        "narrateur|Un croissant pâle reste sur la cuillère.",
    ),
    (3, 2, 1): L(
        "narrateur|Le soir, le papier de Nino claque, comme au préau.",
        "narrateur|Il le secoue au-dessus de la nappe, trop fort.",
        "enfant-m|Le crayon allait dans la flaque !",
        "maman|Ici, pas de flaque. Pose, puis raconte.",
        "narrateur|Nino pose. Le papier s'apaise.",
        "enfant-m|Je l'ai rattrapé, sans attendre. Après, j'ai dessiné un ploc.",
        "maman|Tu as parlé pile pour le crayon. Merci.",
        "papa|Le toit gris, on le voit dans le trait ?",
        "enfant-m|Oui. Et les vraies bottes, elles veulent le radiateur.",
        "narrateur|Maman glisse le vert dans le rond, loin de toute eau.",
        "narrateur|Le croissant de buée montre le trait, net.",
    ),
    (3, 2, 2): L(
        "narrateur|Le soir, papa veut voir le dessin du préau.",
        "enfant-m|Toit gris, point d'eau, crayon mouillé !",
        "narrateur|Les mots tombent pendant qu'il cherche ses lunettes.",
        "papa|Une seconde. Je les ai. Reprends.",
        "narrateur|Nino attend, un pied impatient, puis calme.",
        "enfant-m|J'ai crié, parce que le crayon glissait. J'ai eu raison.",
        "enfant-m|Après, j'ai dessiné le ploc, et les boucles.",
        "papa|Je vois le toit. Je vois le courage.",
        "maman|Le radiateur d'ici peut accueillir un dessin sans rond.",
        "narrateur|Le papier et la botte se rejoignent, sous la lampe.",
        "narrateur|Un croissant de cacao sèche au bord de la tasse.",
    ),
    (3, 2, 3): L(
        "narrateur|Le soir, Nino cache le bonnet loin du courant d'air.",
        "enfant-m|Pas le vent du préau, pas toi.",
        "narrateur|Il veut tout dire d'un souffle. Le bonnet s'échappe.",
        "narrateur|Il le rattrape, et pose le papier d'abord.",
        "enfant-m|Le crayon allait se noyer. J'ai parlé. Puis j'ai dessiné.",
        "enfant-f|Je t'écoute, Nino. Le bonnet aussi.",
        "papa|On a vu le ploc. On a vu les virgules.",
        "maman|Sarah pose le bonnet près des bottes, au sec.",
        "narrateur|Un point d'eau a séché sur le dessin, près du sel.",
        "enfant-m|Plus de flaque. Plus de vent.",
        "narrateur|Le croissant de buée s'arrondit sur la cuillère de Sarah.",
    ),
    (3, 3, 1): L(
        "narrateur|Le soir, Nino entre avec une note du préau, trop haute.",
        "narrateur|La casserole répond, trop basse.",
        "enfant-m|C'est ma chanson de gouttes !",
        "maman|La mienne, c'est le thym. Une après l'autre.",
        "narrateur|Nino se tait. Une botte claque, puis plus.",
        "enfant-m|Sous le toit, j'ai chanté dans l'eau. Après, dans le creux.",
        "maman|Chante-moi le creux, ici.",
        "narrateur|Nino glisse sa note. La vapeur danse, sans ploc.",
        "papa|On pose les bottes sur le dernier mot.",
        "narrateur|Le couplet rentre dans la vapeur, et s'y perd.",
        "enfant-m|Cette fois, ma note a eu le silence.",
    ),
    (3, 3, 2): L(
        "narrateur|Le soir, papa siffle en versant le cacao.",
        "enfant-m|Soleil, soleil !",
        "narrateur|Le sifflet et le couplet se battent, près de la tasse.",
        "papa|Je finis le filet. Ensuite, ta note.",
        "narrateur|Nino attend que le cacao se taise.",
        "enfant-m|Au préau, le ploc a mangé ma note. Après, j'ai eu le creux.",
        "papa|Je prends le creux, maintenant.",
        "maman|La tasse a de la place, pour une note sèche.",
        "narrateur|Papa pose la tasse. La chanson du préau s'endort.",
        "enfant-m|Mes bottes ne claquent plus.",
        "narrateur|Un croissant de vapeur imite celui de l'école.",
    ),
    (3, 3, 3): L(
        "narrateur|Le soir, Sarah tapote le bol, un, deux.",
        "enfant-m|C'est le rythme du préau !",
        "narrateur|Il chante par-dessus. Le bol tressaute.",
        "enfant-f|Un tap, puis l'autre. Le tien après le mien.",
        "narrateur|Nino compte. Il glisse sa note dans le trou.",
        "enfant-m|J'ai chanté dans l'eau. Après, dans le silence.",
        "papa|On a le silence, ici.",
        "maman|Sarah pousse le bol. Le bonnet rouge ne goutte plus.",
        "enfant-f|Toi, tu as le creux. Moi, le bonnet.",
        "narrateur|Sarah chante tout bas, une fois, puis le bol se tait.",
        "narrateur|Les bottes s'endorment, légères, près du bois.",
    ),
}

FINS = {
    (1, 1, 1): L(
        "narrateur|Nino a dit le chuchotis, et le mot du livre.",
        "enfant-m|Tu as eu toute la phrase ?",
        "maman|Toute. Merci.",
        "papa|Les bottes sont légères, maintenant.",
        "narrateur|Le croissant de buée quitte la vitre de la soupe, sans un bruit.",
        "narrateur|Une fibre bleue du tapis brille sous la lampe.",
        "enfant-m|Je raconterai aussi le moment difficile.",
        "maman|Surtout celui-là.",
        "narrateur|Le tic du radiateur s'est tu, très loin.",
    ),
    (1, 1, 2): L(
        "narrateur|Nino a dit le mot, et le point du livre.",
        "papa|J'ai eu le cacao, et tes mots.",
        "maman|Merci d'avoir attendu la tasse.",
        "enfant-m|Mes bottes ne sont plus lourdes.",
        "narrateur|La boucle verte fait clic près de la tasse, puis se tait.",
        "narrateur|Un croissant pâle reste au fond du cacao.",
        "papa|Tu gardes le moment où ça n'allait pas ?",
        "enfant-m|Celui-là, oui.",
        "narrateur|La lampe fait un rond jaune, sur le cuir sec.",
    ),
    (1, 1, 3): L(
        "narrateur|Nino a dit le chuchotis à Sarah.",
        "enfant-f|J'ai eu toute la phrase.",
        "maman|Merci, les deux.",
        "papa|Le bonnet et les bottes sèchent ensemble.",
        "narrateur|Sarah pousse le bol. Le bonnet rouge ne goutte plus.",
        "narrateur|Un croissant de buée s'efface sur la cuillère.",
        "enfant-m|Le moment difficile, je l'ai dit.",
        "enfant-f|Moi, je l'ai gardé.",
        "narrateur|La fibre du tapis reste dans sa tête, tiède.",
    ),
    (1, 2, 1): L(
        "narrateur|Nino a dit les virgules, et l'attente du crayon.",
        "maman|Je vois le trait. Merci.",
        "papa|Les bottes ont leur dessin, près de l'assiette.",
        "enfant-m|Sans colle, le papier est net.",
        "narrateur|Un trait jaune du dessin sèche au bord de l'assiette.",
        "narrateur|Le croissant de buée s'y pose, tout petit.",
        "maman|Tu raconteras le moment où tu as lâché ?",
        "enfant-m|Surtout celui-là.",
        "narrateur|La nappe n'a plus de jaune, plus de vapeur.",
    ),
    (1, 2, 2): L(
        "narrateur|Nino a dit le crayon, et les deux virgules.",
        "papa|Je les vois, près des chaussures.",
        "maman|Merci d'avoir attendu qu'il se tourne.",
        "enfant-m|Le crayon dort, sans rouler.",
        "narrateur|Le cacao laisse un croissant pâle au fond de la tasse.",
        "narrateur|Les bottes et le crayon dorment dans la lumière.",
        "papa|Le moment difficile, tu le gardes ?",
        "enfant-m|Oui. Les deux mains sur le bois.",
        "narrateur|Le dos de papa n'est plus tourné.",
    ),
    (1, 2, 3): L(
        "narrateur|Nino a dit le dessin à Sarah, sans casser le bol.",
        "enfant-f|Le point jaune, c'est pour moi.",
        "papa|Merci d'avoir recommencé, plus bas.",
        "maman|Le bonnet a sa place, près des bottes.",
        "narrateur|Le crayon jaune dort sous le bonnet, sec.",
        "narrateur|Un croissant pâle reste sur le bois du bol.",
        "enfant-m|J'ai failli tout dire d'un coup.",
        "enfant-f|Après, j'ai entendu.",
        "narrateur|Sarah essuie le bout de son nez, tout net.",
    ),
    (1, 3, 1): L(
        "narrateur|Nino a chanté le trou, après la louche.",
        "maman|J'ai eu ta note. Merci.",
        "papa|Les bottes ont suivi le rythme, tout bas.",
        "enfant-m|La soupe n'a pas recouvert la chanson.",
        "narrateur|La casserole chante un dernier toc, puis le silence.",
        "narrateur|Le croissant de buée s'endort sur la vitre.",
        "maman|Tu gardes le couplet trop tôt ?",
        "enfant-m|Surtout celui-là.",
        "narrateur|La vapeur danse, sans recouvrir les mots.",
    ),
    (1, 3, 2): L(
        "narrateur|Nino a chanté les bottes, après le manteau.",
        "papa|J'ai fini, puis toi.",
        "maman|Merci d'avoir laissé le couplet de papa.",
        "enfant-m|Le fil n'a pas cassé, cette fois.",
        "narrateur|Une note de la chanson reste dans la vapeur du cacao.",
        "narrateur|Les boucles vibrent, puis s'arrêtent.",
        "papa|Le moment où ça cassait, tu le dis ?",
        "enfant-m|Oui. Sur le tapis.",
        "narrateur|Le radiateur n'a plus de tic, plus de refrain.",
    ),
    (1, 3, 3): L(
        "narrateur|Nino a donné le trou à Sarah, et la chanson.",
        "enfant-f|J'ai écouté. Puis j'ai eu le bonnet.",
        "maman|Merci, les deux.",
        "papa|Les bottes sont légères, dans la lumière.",
        "narrateur|Sarah tapote le bol, un, deux, puis plus.",
        "narrateur|Un croissant de buée s'endort sur la vitre.",
        "enfant-m|J'ai trop chanté tôt. Après, on m'a entendu.",
        "enfant-f|Moi, j'ai eu le trou.",
        "narrateur|Le bonnet rouge s'arrête, enfin à plat.",
    ),
    (2, 1, 1): L(
        "narrateur|Nino a dit le livre fermé, puis le point.",
        "maman|J'ai tout. Merci.",
        "papa|La botte est loin de la vapeur.",
        "enfant-m|L'assiette d'abord. Mes mots, après.",
        "narrateur|La chaise de la cuisine ne racle plus.",
        "narrateur|La soupe fume, sans toucher le cuir.",
        "maman|Tu raconteras le moment du livre fermé ?",
        "enfant-m|Surtout celui-là.",
        "narrateur|Le croissant de la vitre a de la place, pour lui.",
    ),
    (2, 1, 2): L(
        "narrateur|Nino a dit le livre de la table, jusqu'au point.",
        "papa|J'ai fini ma page. Puis la tienne.",
        "maman|Merci d'avoir attendu le fauteuil.",
        "enfant-m|Cette page-là, elle reste ouverte.",
        "narrateur|Le bois de la table de classe reste dans le cacao, loin.",
        "narrateur|Un croissant de cacao imite celui de la porte.",
        "papa|Le moment où ça claquait, tu le gardes ?",
        "enfant-m|Oui. Deux voix, une page.",
        "narrateur|La botte dort dans le rond de la lampe.",
    ),
    (2, 1, 3): L(
        "narrateur|Nino a rejoué le livre, un mot après l'autre.",
        "enfant-f|La maîtresse du bol a tout entendu.",
        "papa|Nous aussi.",
        "maman|Merci d'avoir rattrapé le bol.",
        "narrateur|Sarah pose une miette sur le bois du bol, sans racle.",
        "narrateur|La lampe leur fait un petit livre de lumière.",
        "enfant-m|J'ai parlé trop vite. Après, j'ai repris.",
        "enfant-f|Moi, j'ai écouté.",
        "narrateur|Le croissant de buée se pose, puis s'efface.",
    ),
    (2, 2, 1): L(
        "narrateur|Nino a dit le nuage de farine, et le trait.",
        "maman|Je vois les boucles. Merci.",
        "papa|Plus de nuage. Des bottes, un croissant.",
        "enfant-m|Le papier est net, sans colle.",
        "narrateur|Le crayon a fini sa course, près du thym de la soupe.",
        "narrateur|Le dessin retrouve sa couleur, dans la lumière.",
        "maman|Tu gardes le moment du pot ?",
        "enfant-m|Surtout celui-là.",
        "narrateur|La farine n'a plus de nuage, plus de saut.",
    ),
    (2, 2, 2): L(
        "narrateur|Nino a dit le pot, le papier, les virgules.",
        "papa|J'ai fini la miche. Puis tes mots.",
        "maman|Merci d'avoir attendu le pain.",
        "enfant-m|Le croissant peut voir la botte.",
        "narrateur|Un croissant de cacao imite celui de la porte.",
        "narrateur|Un trait jaune sèche au bord de la tasse.",
        "papa|Le moment où je coupais, tu le dis ?",
        "enfant-m|Oui. J'ai posé le crayon.",
        "narrateur|Le bois d'ici brille, sans racle.",
    ),
    (2, 2, 3): L(
        "narrateur|Nino a dit le pot à Sarah, sans tirer.",
        "enfant-f|J'ai tout gardé.",
        "papa|Nous aussi, une oreille.",
        "maman|Merci d'avoir raconté, pas dessiné à sa place.",
        "narrateur|Sarah cache le crayon sous le bonnet, pour demain.",
        "narrateur|Un point de farine reste sur le bonnet rouge.",
        "enfant-m|Toi, tu as écouté. Moi, j'ai tracé.",
        "enfant-f|Le croissant, il est tout petit.",
        "narrateur|La botte sèche, près du sel.",
    ),
    (2, 3, 1): L(
        "narrateur|Nino a glissé sa note dans la casserole.",
        "maman|J'ai eu le trou. Merci.",
        "papa|Les bottes attendent le dernier mot.",
        "enfant-m|Deux rythmes, puis le mien.",
        "narrateur|La cuillère de maman fait un dernier toc contre l'émail.",
        "narrateur|Le croissant de la vitre reçoit le vert, sans bruit.",
        "maman|Tu raconteras le couplet trop serré ?",
        "enfant-m|Surtout celui-là.",
        "narrateur|La soupe ne tressaute plus.",
    ),
    (2, 3, 2): L(
        "narrateur|Nino a chanté après le fauteuil.",
        "papa|J'ai fini de m'asseoir. Puis ta note.",
        "maman|Merci. La note a trouvé sa chaise.",
        "enfant-m|Le bois ne tinte plus.",
        "narrateur|Papa souffle sur le cacao. La chanson s'arrête.",
        "narrateur|Un croissant de cacao s'arrondit, puis s'en va.",
        "papa|Le grincement, tu le gardes ?",
        "enfant-m|Oui. Puis le silence.",
        "narrateur|Une botte dort dans le rond, au calme.",
    ),
    (2, 3, 3): L(
        "narrateur|Nino a donné le trou à Sarah, à table.",
        "enfant-f|On a pris notre trou, avec plaisir.",
        "papa|Le silence de Sarah était le plus net.",
        "maman|Merci, les trois notes.",
        "narrateur|Le refrain reste dans le bol, tout au fond.",
        "narrateur|Le bonnet rouge s'arrête, sec.",
        "enfant-m|Chacun sa note.",
        "enfant-f|Toi, les bottes. Moi, le bol.",
        "narrateur|Un croissant de buée s'endort sur le bois.",
    ),
    (3, 1, 1): L(
        "narrateur|Nino a dit la page tachée, puis le coin sec.",
        "maman|Le mot a trouvé sa place. Merci.",
        "papa|On a soufflé sur le point.",
        "enfant-m|Loin de la casserole, ma phrase est entière.",
        "narrateur|La goutte du préau n'atteint plus la vitre de la soupe.",
        "narrateur|Le croissant de buée quitte la vapeur, sans un bruit.",
        "maman|Tu gardes le cri trop tôt ?",
        "enfant-m|Surtout celui-là.",
        "narrateur|La botte, plus sèche, dort dans le rond.",
    ),
    (3, 1, 2): L(
        "narrateur|Nino a dit le ploc, après le clac de la porte.",
        "papa|Je tiens le ploc, maintenant.",
        "maman|Merci d'avoir recommencé.",
        "enfant-m|J'ai laissé la fin, malgré le vent.",
        "narrateur|Le ploc du toit s'est tu. Le cacao ne tremble plus.",
        "narrateur|Un croissant de buée s'ouvre sur le verre de la porte.",
        "papa|Le moment du clac, tu le dis ?",
        "enfant-m|Oui. Puis le silence.",
        "narrateur|Les bottes sèchent, loin de tout toit.",
    ),
    (3, 1, 3): L(
        "narrateur|Nino a réchauffé le bonnet, puis les mots.",
        "enfant-f|Le bord se réchauffe. Tes mots aussi.",
        "papa|On a de la place, près des bottes.",
        "maman|Merci d'avoir repris, plus lentement.",
        "narrateur|Sarah essuie le bord du bol. Plus de goutte.",
        "narrateur|Un croissant pâle reste sur la cuillère.",
        "enfant-m|Plus de vent. Plus de goutte.",
        "enfant-f|Moi, le bonnet. Toi, la phrase.",
        "narrateur|Le point d'eau s'en va, sous le souffle de Sarah.",
    ),
    (3, 2, 1): L(
        "narrateur|Nino a dit le crayon sauvé, puis le ploc dessiné.",
        "maman|Tu as parlé pile. Merci.",
        "papa|Le toit gris, on le voit dans le trait.",
        "enfant-m|Les vraies bottes veulent le radiateur.",
        "narrateur|Un point d'eau a séché sur le dessin, près du sel.",
        "narrateur|Le croissant de buée montre le trait, net.",
        "maman|Le moment de la flaque, tu le gardes ?",
        "enfant-m|Surtout celui-là.",
        "narrateur|Le vert dort dans le rond, loin de toute eau.",
    ),
    (3, 2, 2): L(
        "narrateur|Nino a dit le toit, le courage, les boucles.",
        "papa|Je vois le toit. Je vois le crayon.",
        "maman|Merci d'avoir attendu les lunettes.",
        "enfant-m|J'ai crié pour le crayon. J'ai eu raison.",
        "narrateur|Le papier jaune ne craint plus le ploc, près du cacao.",
        "narrateur|Un croissant de cacao sèche au bord de la tasse.",
        "papa|Le moment du glissement, tu le dis ?",
        "enfant-m|Oui. Puis le dessin.",
        "narrateur|La botte et le papier se rejoignent, sous la lampe.",
    ),
    (3, 2, 3): L(
        "narrateur|Nino a dit le crayon, le vent, le bonnet.",
        "enfant-f|Je t'écoute. Le bonnet aussi.",
        "papa|On a vu le ploc. On a vu les virgules.",
        "maman|Merci d'avoir posé le papier d'abord.",
        "narrateur|Sarah souffle sur le bonnet. Le point d'eau s'en va.",
        "narrateur|Le croissant de buée s'arrondit sur la cuillère de Sarah.",
        "enfant-m|Plus de flaque. Plus de vent.",
        "enfant-f|Moi, au sec. Toi, entendu.",
        "narrateur|Les bottes s'endorment, loin du courant d'air.",
    ),
    (3, 3, 1): L(
        "narrateur|Nino a chanté le creux, après le thym.",
        "maman|J'ai eu ta note. Merci.",
        "papa|Les bottes attendent le dernier mot.",
        "enfant-m|Dans l'eau, puis dans le silence.",
        "narrateur|Le couplet rentre dans la vapeur, et s'y perd.",
        "narrateur|La casserole ne répond plus, trop basse.",
        "maman|Tu gardes la note trop haute ?",
        "enfant-m|Surtout celle-là.",
        "narrateur|Une botte claque, puis plus.",
    ),
    (3, 3, 2): L(
        "narrateur|Nino a chanté après le filet de cacao.",
        "papa|J'ai fini le sifflet. Puis ta note.",
        "maman|Merci. La tasse a de la place.",
        "enfant-m|Mes bottes ne claquent plus.",
        "narrateur|Papa pose la tasse. La chanson du préau s'endort.",
        "narrateur|Un croissant de vapeur imite celui de l'école.",
        "papa|Le ploc qui mangeait, tu le dis ?",
        "enfant-m|Oui. Puis le creux.",
        "narrateur|Le cacao ne siffle plus, plus de bataille.",
    ),
    (3, 3, 3): L(
        "narrateur|Nino a glissé sa note dans le trou de Sarah.",
        "enfant-f|Toi, tu as le creux. Moi, le bonnet.",
        "papa|On a le silence, ici.",
        "maman|Merci, les deux rythmes.",
        "narrateur|Sarah chante tout bas, une fois, puis le bol se tait.",
        "narrateur|Les bottes s'endorment, légères, près du bois.",
        "enfant-m|J'ai chanté dans l'eau. Après, dans le silence.",
        "enfant-f|Moi, j'ai tapoté, puis j'ai écouté.",
        "narrateur|Le bonnet rouge ne goutte plus, plus du tout.",
    ),
}


SONS = {
    "CHK_T0000_P0000": "radiateur,manteau",
    "CHK_T0001_P0001": "tapis",
    "CHK_T0001_P0002": "chaise",
    "CHK_T0001_P0003": "goutte",
}
SONS_T2 = {1: "page", 2: "crayon", 3: "voix_enfant"}
SONS_T3 = {1: "soupe", 2: "cacao", 3: "bol"}
SONS_FIN = {1: "radiateur,silence", 2: "tasse,buée", 3: "bonnet,bol"}

QMETA = {
    1: qf(
        "raconter",
        "raconter | à la maison | écouter | maman | ce soir",
        "Le ventre s'est serré. Que veut-il faire, ce soir ?",
        "Oui, il veut raconter.",
    ),
    2: qf(
        "raconter",
        "raconter | à la maison | écouter | papa | plus tard",
        "Sa phrase s'est perdue. Que veut-il faire, plus tard ?",
        "Oui, il veut raconter.",
    ),
    3: qf(
        "raconter",
        "raconter | à la maison | écouter | maman | la maison",
        "Les gouttes ont couvert sa voix. Que veut-il faire, à la maison ?",
        "Oui, il veut raconter.",
    ),
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("le tapis", "la table", "le préau"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("l'histoire", "le dessin", "la chanson")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[j]
            extras[f"{p2}_T0003_P0000"] = t3("maman", "papa", "la sœur")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = T3[(i, j, k)]
                sons[p3] = SONS_T3[k]
                s[f"{p3}_F0001"] = FINS[(i, j, k)]
                sons[f"{p3}_F0001"] = SONS_FIN[k]
    return s, sons, extras


def path_words(scripts: dict) -> tuple[int, int, float]:
    lengths = []
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                ids = [
                    "CHK_T0000_P0000",
                    "CHK_T0001_P0000",
                    f"CHK_T0001_P000{i}",
                    f"CHK_T0001_P000{i}_Q0001",
                    f"CHK_T0001_P000{i}_C0001",
                    f"CHK_T0001_P000{i}_T0002_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
                ]
                n = 0
                for cid in ids:
                    for ln in scripts[cid]:
                        n += words(ln.split("|", 1)[1])
                lengths.append(n)
    return min(lengths), max(lengths), sum(lengths) / len(lengths)


def write_tree(scripts: dict, sons: dict, extras: dict) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind in ("passage_question", "transition_question") else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        voice(nc, profile_for(cid, kind), extra_note=f"chunk={cid}")
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Nino, Sarah, papa, maman"
    out["setting"] = "école, hall des gouttes, puis la maison"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "si malaise",
        "tout doux",
        "tout calme",
        "il faut demander",
        "on doit demander",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
        "aujourd'hui,",
        "j'ai compris !",
        "mission accomplie",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    if TICS.search(blob):
        raise SystemExit(f"{SID} tic corpus")
    fins = [c["text"] for c in out["chunks"] if c.get("kind") == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"{SID} fins distinctes: {len(set(fins))}/{len(fins)}")
    t3s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage" and "_T0003_P000" in c["chunk_id"] and not c["chunk_id"].endswith("_P0000")
    ]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"{SID} T3 distincts: {len(set(t3s))}/{len(t3s)}")
    t2s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage" and "_T0002_P000" in c["chunk_id"] and c["chunk_id"].endswith(("P0001", "P0002", "P0003")) and "_T0003" not in c["chunk_id"]
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"{SID} T2 distincts: {len(set(t2s))}/{len(t2s)}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    lo, hi, avg = path_words(scripts)
    if lo < 520 or hi > 720:
        raise SystemExit(f"{SID} chemins hors cible: {lo}–{hi} (moyenne {avg:.0f})")
    print(f"chemins {lo}–{hi} mots (moyenne {avg:.0f})")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    s, n, e = build()
    write_tree(s, n, e)
    lo, hi, avg = path_words(s)
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Pas d'apply.\n\n"
        "## Promesse narrative\n\n"
        "La paume de papa chauffe la poignée : la porte vitrée s'embue. "
        "Un croissant de buée s'y dessine, à hauteur des bottes vertes de Nino. "
        "Il veut les poser au radiateur et ramener le bonnet de Sarah. "
        "Il parle trop tôt : on n'entend que « lourdes ». Tapis, table ou préau "
        "changent l'obstacle. Histoire, dessin ou chanson changent la deuxième ruse. "
        "Maman, papa ou Sarah changent l'oreille du soir. Le croissant paie la fin.\n\n"
        "## Vécu\n\n"
        "Nino veut poser ses bottes au radiateur du hall des gouttes, ramener "
        "le bonnet rouge, et garder une phrase qui pince. Première tentative : "
        "il parle pendant maman. Le croissant avale la fin. Tapis (chuchotis), "
        "table (racle) ou préau (ploc) changent l'échec. Histoire, dessin ou "
        "chanson changent la ruse : page coupée, crayon tiré, couplet trop tôt "
        "(sauf la goutte vers le crayon, où parler pile sauve le papier). "
        "Le soir, cuillère, tasse ou mâche recouvrent les mots ; il attend ; "
        "le croissant revient. 27 fins : bottes légères, croissant payé. "
        f"Chemins {lo}–{hi} mots (moyenne {avg:.0f}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Nino, Sarah, papa, maman.\n"
        "- 86 nœuds, graphe et libellés d'options conservés.\n"
        "- 27 fins textuellement distinctes, 27 T3 distincts, 9 T2 distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Indice unique dès l'ouverture : le croissant de buée, payé au climax.\n"
        "- Objet indispensable : les bottes (lourdes, virgules d'eau, boucles). Bonnet de Sarah gardé.\n"
        "- Leçon COL.ECO.001 vécue, non dite : attendre le creux ; ce qui serre se raconte le soir.\n"
        "- Un merci vécu (T1), pas un refrain Bravo / bon travail.\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N2 ≤ 15 mots/phrase. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Ouverture : paume sur la poignée (pas les cinq gabarits v2).\n"
        "- P1 F-NAR-019. Pas apply. Pas audio.\n\n"
        "## Direction vocale\n\n"
        "`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        "tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. Tours "
        "de parole : envie de couper, retenue, écoute réelle, plaisir d'être entendu.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
