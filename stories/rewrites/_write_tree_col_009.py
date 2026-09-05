#!/usr/bin/env python3
"""TREE-COL-009 — Le bouton rouge de Nina. F-NAR-019 / example4 v2. Texte seulement."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, make_chunk, words  # noqa: E402

SID = "TREE-COL-009"
N3 = LIMITS["N3"]
TICS = (
    "tout doux",
    "tout calme",
    "on lève la main",
    "puis on parle",
    "on va apprendre",
    "maîtresse",
    "maitresse",
)
TIC_WORDS = re.compile(r"\b(encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note="arc=installation; intention=faire_sentir_le_trou_vide; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_bouton_attend_au_crochet; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=le_rouge_a_roule; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; destinataire=enfant; sous_texte=aniss_a_ete_entendu; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_parle_par_dessus; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=deux_envies_en_meme_temps; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=la_virgule_de_fil_paie; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_manteau_tient_le_bouton; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out = []
    for raw in rows:
        raw = raw.strip()
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic «{tic}»: {ph}")
        if TIC_WORDS.search(ph):
            raise SystemExit(f"tic mot: {ph}")
        out.append(f"{role}|{ph}")
    return list(out)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp and emp in text:
        e = esc(emp)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
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
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return f"{body}{tail}".strip()


def voice(nc: dict, profile: str, emphasis: str | None, sons: str) -> None:
    m = dict(PROFILES[profile])
    m["emphasis"] = emphasis
    text = nc["text"]
    nc["sons"] = sons or ""
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitch_ssml"]
    nc["pitch_xai_tag"] = m["pitch_tag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = emphasis or ""
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
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"


def t3labs(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    prof: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    def put(cid: str, lines: list[str], profile: str, son: str, emp: str | None = None) -> None:
        s[cid] = lines
        sons[cid] = son
        prof[cid] = profile
        emph[cid] = emp

    put(
        "CHK_T0000_P0000",
        L(
            "narrateur|Le pouce de Nina cherche un rond, sur son manteau.",
            "narrateur|Le trou est vide, un peu froid.",
            "narrateur|Le radiateur de la classe fait tic.",
            "narrateur|Ça sent la cire des crayons, et le savon.",
            "narrateur|Au crochet, un bouton rouge attend.",
            "narrateur|Un fil blanc en pend, plié en virgule.",
            "enfant-f|Toi, je te remets avant la cour !",
            "papa|C'est quoi, ce fil ?",
            "enfant-f|Une virgule.",
            "narrateur|En ce moment, Aniss arrive près du tapis.",
            "enfant-m|Moi, je commence la route !",
            "enfant-f|Non, le bouton d'abord !",
            "narrateur|Nina parle par-dessus la phrase d'Aniss.",
            "narrateur|Elle tire le bouton trop vite.",
            "narrateur|Le fil glisse.",
            "narrateur|Le rouge tombe.",
            "narrateur|Il roule sous le radiateur, tic.",
            "enfant-f|Il part !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Envie et inquiétude se bousculent, dans sa poitrine.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Il tourne le visage vers Aniss.",
            "enfant-m|La route va jusqu'à la cour.",
            "narrateur|Nina attend, les joues chaudes.",
            "enfant-f|Pardon.",
            "maman|Quel jeu pour remettre le bouton ?",
        ),
        "opening",
        "radiateur,manteau",
        "bouton rouge",
    )
    put(
        "CHK_T0001_P0000",
        L(
            "narrateur|Les cubes, le livre, ou la dînette.",
            "maman|Quel jeu pour le bouton ?",
        ),
        "choice",
        "",
        None,
    )
    extras["CHK_T0001_P0000"] = t3labs("les cubes", "le livre", "la dînette")

    put(
        "CHK_T0001_P0001",
        L(
            "narrateur|Nina s'assoit près des cubes, sur le tapis.",
            "narrateur|Ils sont en bois, un peu rudes.",
            "narrateur|Elle pose le bouton sur un cube rouge.",
            "enfant-f|Ça, c'est le toit de la tour !",
            "enfant-m|Attends, ma route n'est pas finie.",
            "narrateur|Nina empile plus haut, sans écouter.",
            "narrateur|La tour penche.",
            "narrateur|Le bouton bascule.",
            "narrateur|Il tape le tapis, toc.",
            "enfant-f|Ma tour !",
            "narrateur|Aniss pose sa dernière brique, sans crier.",
            "narrateur|Nina ramasse le rouge, les mains tremblantes.",
            "papa|Tu veux que je tienne un cube ?",
            "enfant-f|Oui, le bas.",
            "narrateur|Elle laisse Aniss pousser sa route.",
            "enfant-m|Voilà, elle va à la cour.",
            "enfant-f|Alors le toit, maintenant.",
            "maman|Le fil fait toujours sa virgule.",
            "narrateur|Le bouton tient au sommet, un peu de travers.",
        ),
        "action",
        "cubes,bois",
        "cubes",
    )
    put(
        "CHK_T0001_P0001_Q0001",
        L(
            "narrateur|Quelque chose de rouge a tapé le tapis.",
            "maman|Qu'est-ce qui est tombé de la tour ?",
        ),
        "clue",
        "",
        "bouton",
    )
    extras["CHK_T0001_P0001_Q0001"] = qf(
        "bouton",
        "bouton | le bouton | bouton rouge | le bouton rouge",
        "Un rond rouge a fait toc. C'était quoi ?",
    )
    put(
        "CHK_T0001_P0001_C0001",
        L(
            "enfant-f|Le bouton rouge !",
            "narrateur|Oui, le bouton.",
            "narrateur|Il a fait toc.",
            "narrateur|Aniss a fini sa route, cette fois.",
            "papa|Merci d'avoir laissé la dernière brique.",
            "maman|On goûte, avec le bouton ?",
            "enfant-f|Oui.",
        ),
        "confirm",
        "cubes",
        "bouton rouge",
    )

    put(
        "CHK_T0001_P0002",
        L(
            "narrateur|Nina ouvre le livre près de la fenêtre.",
            "narrateur|La couverture est un peu rêche.",
            "narrateur|Elle glisse le bouton dans le pli.",
            "enfant-f|Regarde, le manteau de l'histoire !",
            "enfant-m|J'étais en train de dire la page.",
            "narrateur|Nina parle plus fort, par-dessus.",
            "narrateur|La page glisse.",
            "narrateur|Le bouton tombe dans le pli.",
            "enfant-f|Il est coincé !",
            "narrateur|Aniss reprend, plus bas.",
            "enfant-m|La page, c'était un bateau.",
            "narrateur|Nina attend la fin du bateau.",
            "papa|Je peux tourner, après ?",
            "enfant-f|Après sa phrase.",
            "maman|Le fil blanc dépasse du pli.",
            "narrateur|Nina pince le fil, sans tirer.",
            "enfant-f|Je te sors, tout petit.",
            "narrateur|Le bouton repose sur le bateau dessiné.",
        ),
        "action",
        "pages,papier",
        "livre",
    )
    put(
        "CHK_T0001_P0002_Q0001",
        L(
            "narrateur|Un fil blanc dépasse du pli du livre.",
            "papa|Qu'est-ce qui était coincé dans la page ?",
        ),
        "clue",
        "",
        "bouton",
    )
    extras["CHK_T0001_P0002_Q0001"] = qf(
        "bouton",
        "bouton | le bouton | bouton rouge | le bouton rouge",
        "Le fil dépasse du pli. Qu'est-ce ?",
    )
    put(
        "CHK_T0001_P0002_C0001",
        L(
            "enfant-f|Le bouton !",
            "narrateur|Oui, le bouton du pli.",
            "narrateur|Aniss a fini son bateau.",
            "papa|Merci d'avoir attendu la page.",
            "maman|On goûte, le livre fermé ?",
            "enfant-f|Oui.",
            "narrateur|La virgule de fil brille sur la couverture.",
        ),
        "confirm",
        "pages",
        "bouton",
    )

    put(
        "CHK_T0001_P0003",
        L(
            "narrateur|Nina pose une tasse de dînette, froide.",
            "narrateur|Elle y met le bouton, comme un gâteau.",
            "enfant-f|C'est la cerise du goûter !",
            "enfant-m|Je verse, attends.",
            "narrateur|Nina tape la tasse pour qu'on la voie.",
            "narrateur|La cuillère d'Aniss penche.",
            "narrateur|L'eau pour de rire fuit.",
            "enfant-m|Ma soupe !",
            "narrateur|Le bouton roule dans la soucoupe.",
            "enfant-f|Pardon, je tapais.",
            "narrateur|Aniss finit de verser, tout droit.",
            "papa|On tient la tasse à deux ?",
            "enfant-f|Oui, après sa soupe.",
            "maman|Le fil fait une virgule, dans l'assiette.",
            "narrateur|Nina pose le rouge, sans taper.",
            "enfant-f|Cerise, maintenant.",
            "narrateur|La tasse ne tremble plus.",
        ),
        "action",
        "tasse,bois",
        "dînette",
    )
    put(
        "CHK_T0001_P0003_Q0001",
        L(
            "narrateur|Un rond rouge a roulé dans la soucoupe.",
            "maman|Qu'est-ce que Nina posait comme cerise ?",
        ),
        "clue",
        "",
        "bouton",
    )
    extras["CHK_T0001_P0003_Q0001"] = qf(
        "bouton",
        "bouton | le bouton | bouton rouge | le bouton rouge | cerise",
        "La cerise du goûter était rouge. C'était quoi ?",
    )
    put(
        "CHK_T0001_P0003_C0001",
        L(
            "enfant-f|Le bouton rouge !",
            "narrateur|Oui, la cerise de la tasse.",
            "narrateur|Aniss a versé jusqu'au bout.",
            "papa|Merci d'avoir laissé la soupe.",
            "maman|On goûte pour de vrai, maintenant ?",
            "enfant-f|Oui.",
            "narrateur|Le fil blanc reste plié, dans l'assiette.",
        ),
        "confirm",
        "tasse",
        "bouton rouge",
    )

    t2_choice = {
        1: L(
            "narrateur|Près des cubes, trois goûters attendent.",
            "papa|Une pomme, un yaourt, ou du pain ?",
            "maman|On partage avec quoi ?",
        ),
        2: L(
            "narrateur|Près du livre, trois goûters attendent.",
            "papa|Une pomme, un yaourt, ou du pain ?",
            "maman|On partage avec quoi ?",
        ),
        3: L(
            "narrateur|Près de la dînette, trois goûters attendent.",
            "papa|Une pomme, un yaourt, ou du pain ?",
            "maman|On partage avec quoi ?",
        ),
    }

    t2_pass = {
        (1, 1): L(
            "narrateur|Nina croque la pomme, trop vite.",
            "narrateur|Elle veut raconter le toit des cubes.",
            "enfant-f|Le bouton était en haut !",
            "enfant-m|Moi, je coupe d'abord.",
            "narrateur|Les deux voix se mêlent.",
            "narrateur|La pomme glisse vers le tapis.",
            "narrateur|Elle heurte un cube, puis s'arrête.",
            "enfant-f|Elle partait !",
            "narrateur|Nina referme la bouche.",
            "narrateur|Aniss coupe une part, sans se presser.",
            "papa|Tu veux le quartier d'Aniss, ou le tien ?",
            "enfant-f|Le mien, après sa part.",
            "maman|Le fil a pris un éclat de pomme.",
            "narrateur|Nina mange, puis tend le bouton, sans parler.",
        ),
        (1, 2): L(
            "narrateur|Nina ouvre le yaourt près des cubes.",
            "narrateur|La cuillère cliquette contre le pot.",
            "enfant-f|Le toit, c'était le bouton !",
            "enfant-m|J'ai pas eu la cuillère.",
            "narrateur|Nina parle et mélange en même temps.",
            "narrateur|Une goutte blanche tombe sur un cube.",
            "enfant-f|Oh.",
            "narrateur|Elle pose la cuillère.",
            "narrateur|Aniss mélange, lentement, jusqu'au fond.",
            "papa|On goûte après son tour ?",
            "enfant-f|Oui.",
            "maman|Le fil a une perle de yaourt.",
            "narrateur|Nina attend la cuillère, les mains calmes.",
            "enfant-f|À moi, maintenant.",
        ),
        (1, 3): L(
            "narrateur|Nina casse le pain au-dessus des cubes.",
            "narrateur|Des miettes tombent dans la route d'Aniss.",
            "enfant-f|Le bouton tenait tout seul !",
            "enfant-m|Ma route, les miettes.",
            "narrateur|Nina voulait tout dire d'un coup.",
            "narrateur|Le pain chaud lui brûle un peu la lèvre.",
            "narrateur|Elle s'arrête.",
            "narrateur|Aniss souffle sur sa croûte.",
            "papa|On partage la croûte, ou la mie ?",
            "enfant-f|La mie, après son souffle.",
            "maman|Une miette dort sur le fil blanc.",
            "narrateur|Nina tend un morceau, sans couper la phrase.",
            "enfant-m|Merci, la route est propre.",
        ),
        (2, 1): L(
            "narrateur|Nina pose la pomme sur le livre fermé.",
            "narrateur|Elle veut raconter le bateau de la page.",
            "enfant-f|Le bouton était dans le pli !",
            "enfant-m|Moi, je disais le bateau.",
            "narrateur|La pomme roule sur la couverture.",
            "narrateur|Elle laisse un rond humide.",
            "enfant-f|La page va coller !",
            "narrateur|Nina reprend le fruit, sans crier.",
            "narrateur|Aniss finit le mot bateau.",
            "papa|On coupe, maintenant ?",
            "enfant-f|Oui, sa phrase est finie.",
            "maman|Le fil sent un peu la pomme.",
            "narrateur|Ils croquent, le livre à l'abri.",
        ),
        (2, 2): L(
            "narrateur|Nina pose le yaourt contre le livre.",
            "narrateur|Le pot est frais, tout lisse.",
            "enfant-f|Le pli a gardé le bouton !",
            "enfant-m|Je voulais ouvrir le couvercle.",
            "narrateur|Nina tire le couvercle pendant qu'il parle.",
            "narrateur|Une goutte file vers la reliure.",
            "enfant-f|Pas sur le bateau !",
            "narrateur|Elle essuie du pouce, sans un mot.",
            "narrateur|Aniss ouvre, cette fois, jusqu'au bout.",
            "papa|La cuillère, à qui ?",
            "enfant-f|À lui, une seconde.",
            "maman|Le fil a une perle blanche.",
            "narrateur|Nina goûte après, la page sèche.",
        ),
        (2, 3): L(
            "narrateur|Nina émiette le pain près du livre.",
            "narrateur|Une miette glisse dans le pli.",
            "enfant-f|Le bouton était là !",
            "enfant-m|J'avais une histoire de croûte.",
            "narrateur|Nina parle la bouche pleine.",
            "narrateur|Aniss n'entend que des miettes.",
            "narrateur|Elle avale, les joues chaudes.",
            "narrateur|Aniss dit sa croûte, jusqu'à la fin.",
            "papa|On garde une miette pour le fil ?",
            "enfant-f|Une seule, tout petit.",
            "maman|Le livre sent le pain chaud.",
            "narrateur|Nina tend la croûte, puis écoute.",
        ),
        (3, 1): L(
            "narrateur|Nina pose la pomme dans l'assiette de dînette.",
            "narrateur|Elle veut raconter la cerise rouge.",
            "enfant-f|C'était le bouton !",
            "enfant-m|Moi, je servais les parts.",
            "narrateur|Nina coupe trop tôt.",
            "narrateur|Un quartier file sous la tasse.",
            "enfant-f|Il se cache !",
            "narrateur|Elle recule les mains.",
            "narrateur|Aniss sert, une part, puis l'autre.",
            "papa|On cherche le quartier, après son service ?",
            "enfant-f|Après.",
            "maman|Le fil a un jus de pomme, minuscule.",
            "narrateur|Nina croque quand les assiettes sont prêtes.",
        ),
        (3, 2): L(
            "narrateur|Nina verse le yaourt dans la petite tasse.",
            "narrateur|Ça déborde, un filet blanc.",
            "enfant-f|La cerise, c'était le bouton !",
            "enfant-m|J'avais la cuillère de service.",
            "narrateur|Nina parle et verse en même temps.",
            "narrateur|La tasse déborde sur la soucoupe.",
            "enfant-f|Trop !",
            "narrateur|Elle pose le pot.",
            "narrateur|Aniss essuie, puis sert, sans se presser.",
            "papa|On goûte dans quelle tasse ?",
            "enfant-f|La sienne, d'abord.",
            "maman|Le fil a une perle, au bord.",
            "narrateur|Nina attend sa tasse, les épaules plus basses.",
        ),
        (3, 3): L(
            "narrateur|Nina pose le pain dans la casserole de dînette.",
            "narrateur|Elle veut en faire un gâteau.",
            "enfant-f|Avec le bouton sur le dessus !",
            "enfant-m|Je mélangeais, moi.",
            "narrateur|Nina pousse le pain trop fort.",
            "narrateur|Des miettes sautent dans la soupe pour de rire.",
            "enfant-m|Ma soupe !",
            "narrateur|Nina recule la casserole.",
            "narrateur|Aniss mélange, trois tours, puis s'arrête.",
            "papa|On met le gâteau, là ?",
            "enfant-f|Oui, son mélange est fini.",
            "maman|Une miette tient au fil blanc.",
            "narrateur|Nina pose le pain, sans bousculer.",
        ),
    }

    t3_choice = {
        1: L(
            "narrateur|La cour des trois marches sent l'herbe.",
            "papa|Le chat, le chien, ou la poule ?",
            "maman|Qui vois-tu, là-bas ?",
        ),
        2: L(
            "narrateur|La cour des trois marches est un peu humide.",
            "papa|Le chat, le chien, ou la poule ?",
            "maman|Qui s'approche du goûter ?",
        ),
        3: L(
            "narrateur|La cour des trois marches a des cailloux.",
            "papa|Le chat, le chien, ou la poule ?",
            "maman|Qui picore près des marches ?",
        ),
    }

    t3_pass = {
        (1, 1): L(
            "narrateur|Nina descend les trois marches, la pomme à l'autre main.",
            "narrateur|Un chat gris se frotte au premier degré.",
            "enfant-m|Moi, je le caresse !",
            "enfant-f|Le bouton, d'abord !",
            "narrateur|Elle avance trop vite.",
            "narrateur|Le chat bondit.",
            "narrateur|Le fil blanc file sous une marche.",
            "enfant-f|Il disparaît !",
            "narrateur|Nina s'arrête.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Elle écoute : un ronron, sous la pierre.",
            "narrateur|La virgule de fil brille, au bord.",
            "enfant-f|Je te vois.",
            "narrateur|Aniss finit d'appeler le chat, tout bas.",
            "narrateur|Le chat ressort.",
            "narrateur|Le bouton aussi, avec un poil gris.",
            "papa|Le fil est là.",
            "enfant-f|Il faisait sa virgule.",
        ),
        (1, 2): L(
            "narrateur|Nina tient pomme et bouton, dans la cour.",
            "narrateur|Un chien brun pose le museau près du fruit.",
            "enfant-m|Il veut jouer avec moi !",
            "enfant-f|Pas le bouton !",
            "narrateur|Elle tire le fil.",
            "narrateur|Le chien saisit le rouge, tout léger.",
            "enfant-f|Rends-le !",
            "narrateur|Le mot tombe pendant qu'Aniss siffle.",
            "narrateur|Le chien ne lâche rien.",
            "narrateur|Nina recule les mains.",
            "narrateur|Elle écoute le souffle du chien, puis le sifflet.",
            "narrateur|La virgule de fil pend au coin des lèvres.",
            "enfant-f|Je la vois, la virgule.",
            "narrateur|Aniss siffle jusqu'au bout.",
            "narrateur|Le chien pose le bouton, un peu humide.",
            "papa|Il l'a rendu.",
            "enfant-f|Quand on a fini le sifflet.",
        ),
        (1, 3): L(
            "narrateur|Nina pose la pomme sur la dernière marche.",
            "narrateur|Une poule rousse picore tout près.",
            "enfant-m|Elle vient pour moi !",
            "enfant-f|Elle veut le fil !",
            "narrateur|Nina tire le bouton vers elle.",
            "narrateur|La poule pique la virgule blanche.",
            "enfant-f|Aïe, le fil !",
            "narrateur|Presque avalé.",
            "narrateur|Nina ouvre la main, au lieu de tirer.",
            "narrateur|Elle écoute le cot, puis le silence.",
            "narrateur|La virgule de fil brille au bec, une seconde.",
            "enfant-f|Là, comme au crochet.",
            "narrateur|Aniss reste immobile, sa phrase finie.",
            "narrateur|La poule lâche le fil, une plume reste.",
            "papa|Le bouton est libre.",
            "enfant-f|J'ai failli trop tirer.",
        ),
        (2, 1): L(
            "narrateur|Nina descend avec le pot de yaourt.",
            "narrateur|Le chat se couche sur la première marche.",
            "enfant-m|Je le prends sur les genoux !",
            "enfant-f|Il est sur mon bouton !",
            "narrateur|Elle pousse le chat du poignet.",
            "narrateur|Le pot penche.",
            "narrateur|Le chat part sous les marches, le rouge avec.",
            "enfant-f|Les deux !",
            "narrateur|Nina s'agenouille, sans plonger le bras.",
            "narrateur|Elle écoute le ronron, tout près de la pierre.",
            "narrateur|La virgule de fil luit dans l'ombre.",
            "enfant-f|Je te vois, virgule.",
            "narrateur|Aniss attend, les genoux pliés, sans appeler.",
            "narrateur|Le chat sort, une perle blanche au poil.",
            "papa|Le bouton a suivi le fil.",
            "enfant-f|Comme au crochet, ce matin.",
        ),
        (2, 2): L(
            "narrateur|Nina pose le yaourt au bas des marches.",
            "narrateur|Un chien tourne autour du pot.",
            "enfant-m|Il aime le lait, avec moi !",
            "enfant-f|Pas lécher le bouton !",
            "narrateur|Elle cache le rouge derrière le dos.",
            "narrateur|Le chien pose une patte sur le pot.",
            "narrateur|Le bouton glisse, coincé sous le coussinet.",
            "enfant-f|Dessous !",
            "narrateur|Nina ne tire pas.",
            "narrateur|Elle écoute Aniss compter, tout bas.",
            "enfant-m|Un, deux, patte.",
            "narrateur|La virgule de fil dépasse entre les doigts du chien.",
            "enfant-f|Le fil, je le vois.",
            "narrateur|Le chien lève la patte, le compte fini.",
            "papa|Le rouge est libre.",
            "enfant-f|On a compté ensemble.",
        ),
        (2, 3): L(
            "narrateur|Nina tient le yaourt loin des cailloux.",
            "narrateur|La poule picore le couvercle tombé.",
            "enfant-m|Elle est à moi, la poule !",
            "enfant-f|Elle picore le fil !",
            "narrateur|Nina souffle trop fort.",
            "narrateur|La poule s'envole d'un mètre, le fil au bec.",
            "enfant-f|Reviens !",
            "narrateur|Le bouton pend, presque perdu.",
            "narrateur|Nina se tait.",
            "narrateur|Elle écoute les ailes, puis plus rien.",
            "narrateur|La virgule blanche dessine un arc, au soleil.",
            "enfant-f|Comme au crochet.",
            "narrateur|Aniss tend une miette de silence, les mains ouvertes.",
            "narrateur|La poule pose le bouton près du pot.",
            "papa|Il a failli partir.",
            "enfant-f|J'ai arrêté de souffler.",
        ),
        (3, 1): L(
            "narrateur|Nina descend avec le pain, des miettes derrière elle.",
            "narrateur|Le chat suit la piste, jusqu'au bouton.",
            "enfant-m|Il joue avec moi !",
            "enfant-f|Pas avec le fil !",
            "narrateur|Elle secoue le pain pour chasser le chat.",
            "narrateur|Plus de miettes, plus de chat, plus de rouge.",
            "enfant-f|Où es-tu ?",
            "narrateur|Nina s'assoit sur la marche du milieu.",
            "narrateur|Elle écoute l'herbe, un froissement minuscule.",
            "narrateur|La virgule de fil bouge entre deux brins.",
            "enfant-f|Là, comme ce matin.",
            "narrateur|Aniss finit sa phrase aux miettes, sans bouger.",
            "narrateur|Le chat ramène le bouton, un brin d'herbe au fil.",
            "papa|Il te l'a rendu.",
            "enfant-f|J'ai cessé de secouer.",
        ),
        (3, 2): L(
            "narrateur|Nina tient le pain contre le manteau ouvert.",
            "narrateur|Un chien sent la croûte, puis le fil.",
            "enfant-m|On joue à attraper !",
            "enfant-f|Pas le bouton !",
            "narrateur|Elle lance un morceau trop loin.",
            "narrateur|Le chien part, le rouge coincé dans la croûte.",
            "enfant-f|Les deux partent !",
            "narrateur|Nina reste sur la marche, les pieds collés.",
            "narrateur|Elle écoute les griffes sur les cailloux.",
            "narrateur|Puis plus rien, sauf un fil blanc, au loin.",
            "enfant-f|La virgule, je la vois.",
            "narrateur|Aniss appelle le chien, une fois, jusqu'au bout.",
            "narrateur|Le chien revient, la croûte mâchée, le bouton sain.",
            "papa|Le fil a tenu.",
            "enfant-f|J'ai failli tout lancer.",
        ),
        (3, 3): L(
            "narrateur|Nina émiette le pain au bas des marches.",
            "narrateur|La poule arrive, pressée.",
            "enfant-m|Je lui donne, moi !",
            "enfant-f|Moi aussi, et le bouton !",
            "narrateur|Deux mains, trop de miettes.",
            "narrateur|La poule pique le fil et une miette ensemble.",
            "enfant-f|Le rouge s'envole !",
            "narrateur|Nina ouvre les doigts, au lieu de fermer.",
            "narrateur|Elle écoute le cot cot, puis le vent.",
            "narrateur|La virgule de fil dessine un S, dans l'air.",
            "enfant-f|C'est la même, du crochet.",
            "narrateur|Aniss pose sa dernière miette, sans parler.",
            "narrateur|La poule lâche le bouton sur un caillou.",
            "papa|Il a failli devenir grain.",
            "enfant-f|J'ai ouvert la main.",
        ),
    }

    t1_echo = {
        1: L(
            "narrateur|Dans la poche, un cube a une petite bosse.",
        ),
        2: L(
            "narrateur|La page du livre garde une odeur de papier.",
        ),
        3: L(
            "narrateur|La petite tasse a laissé un rond, au fond.",
        ),
    }

    ends = {
        (1, 1, 1): L(
            "narrateur|Sur la marche du haut, Nina recoud le bouton.",
            "narrateur|Papa tient le manteau ouvert, sans parler.",
            "narrateur|Un poil de chat reste dans la virgule de fil.",
            "narrateur|Le cube bosselé dort dans la poche.",
            "enfant-f|Il tient, le rond.",
            "maman|Ton manteau ferme, maintenant ?",
            "enfant-f|Oui.",
            "narrateur|La pomme a laissé un éclat, sur le rouge.",
            "narrateur|Le radiateur, loin, fait un dernier tic.",
            "narrateur|Le manteau ne baille plus.",
        ),
        (1, 1, 2): L(
            "narrateur|Nina glisse le bouton dans la boutonnière.",
            "narrateur|Le museau du chien a laissé un rond humide.",
            "narrateur|Elle essuie, puis pousse le fil en virgule.",
            "papa|Il rentre, ce rond ?",
            "enfant-f|Oui, tout droit.",
            "maman|La pomme a marqué un petit croissant.",
            "narrateur|Le cube de la poche cogne, une fois.",
            "narrateur|Ils s'assoient sur la marche du milieu.",
            "narrateur|Le manteau ferme sur le rouge, un peu froid.",
        ),
        (1, 1, 3): L(
            "narrateur|Nina accroche le bouton au crochet de la cour.",
            "narrateur|Une plume rousse tient à la virgule de fil.",
            "enfant-f|Comme ce matin, mais dehors.",
            "papa|On le remet au manteau, après ?",
            "enfant-f|Après la plume.",
            "maman|La pomme a un trou de bec, minuscule.",
            "narrateur|Le cube bosselé reste dans la main d'Aniss.",
            "narrateur|Le crochet de la cour garde le rouge, au soleil.",
        ),
        (1, 2, 1): L(
            "narrateur|Nina pose le bouton sur le rebord de la fenêtre.",
            "narrateur|Une perle de yaourt sèche sur le fil.",
            "narrateur|Un poil gris s'y colle.",
            "papa|On le coud, ou on attend ?",
            "enfant-f|On attend que ça sèche.",
            "maman|Le cube a une goutte blanche, lui aussi.",
            "narrateur|Le manteau reste ouvert une minute, puis ferme.",
            "narrateur|La perle devient un grain mat, sur la virgule.",
        ),
        (1, 2, 2): L(
            "narrateur|Nina s'assoit sur le banc de la cour.",
            "narrateur|Le bouton porte l'empreinte d'une patte.",
            "narrateur|Le yaourt a laissé un croissant blanc.",
            "enfant-f|C'est sa virgule, à lui.",
            "papa|On la garde, cette marque ?",
            "enfant-f|Oui.",
            "maman|Le cube de la poche sent le lait.",
            "narrateur|Elle pousse le bouton dans le trou du manteau.",
            "narrateur|Le banc garde un rond blanc, tout petit.",
        ),
        (1, 2, 3): L(
            "narrateur|Nina range le bouton dans le cartable.",
            "narrateur|Une plume et une perle de yaourt voyagent ensemble.",
            "enfant-f|Ils se touchent, dans la poche.",
            "papa|On le coud à la maison ?",
            "enfant-f|Oui, le fil est long.",
            "maman|Le cube bosselé rentre aussi ?",
            "enfant-f|Oui, près du rouge.",
            "narrateur|Le cartable garde la plume et la perle, au chaud.",
        ),
        (1, 3, 1): L(
            "narrateur|Nina recoud près du radiateur, de retour.",
            "narrateur|Une miette et un poil de chat partagent le fil.",
            "papa|Il pique, l'aiguille ?",
            "enfant-f|Un peu.",
            "maman|Le cube a une miette dans une fente.",
            "narrateur|Le tic du radiateur accompagne le dernier point.",
            "narrateur|Le manteau ferme.",
            "narrateur|La virgule de fil disparaît dans le tissu.",
        ),
        (1, 3, 2): L(
            "narrateur|Nina s'assoit dans la poussière des trois marches.",
            "narrateur|Le bouton a une croûte collée, et un poil de chien.",
            "enfant-f|Il sent le pain.",
            "papa|On le brosse, avant le trou ?",
            "enfant-f|Oui.",
            "maman|Le cube a pris un grain de pain, lui aussi.",
            "narrateur|Elle brosse, puis pousse le rouge dans le rond.",
            "narrateur|La poussière des marches reste au fil, un peu.",
        ),
        (1, 3, 3): L(
            "narrateur|Nina glisse le bouton dans le trou du manteau.",
            "narrateur|Une miette reste coincée, avec une plume.",
            "enfant-f|Ça gratte, un tout petit peu.",
            "papa|On la sort, la miette ?",
            "enfant-f|Non, elle raconte la poule.",
            "maman|Et le cube ?",
            "enfant-f|Dans la poche, avec sa bosse.",
            "narrateur|Le manteau tient.",
            "narrateur|La virgule de fil dépasse, comme un secret.",
        ),
        (2, 1, 1): L(
            "narrateur|Nina pose le livre sur ses genoux, dans la cour.",
            "narrateur|Le bouton revient sur le bateau dessiné.",
            "narrateur|Un poil de chat traverse la virgule de fil.",
            "papa|On le coud, ou on le laisse voyager ?",
            "enfant-f|On le coud, le bateau a fini.",
            "maman|La pomme a laissé un rond sur la couverture.",
            "narrateur|Le manteau se ferme par-dessus la page.",
            "narrateur|Le bateau garde une ombre rouge, minuscule.",
        ),
        (2, 1, 2): L(
            "narrateur|Nina essuie le bouton au plat de la page.",
            "narrateur|Le museau du chien a mouillé le rouge.",
            "narrateur|La pomme a parfumé le papier.",
            "enfant-f|Ça sent le fruit, et le chien.",
            "papa|Le fil rentre ?",
            "enfant-f|Oui, en virgule.",
            "maman|La buée de la vitre n'est plus là.",
            "narrateur|Le manteau ferme.",
            "narrateur|La page garde un goût de pomme, tout bas.",
        ),
        (2, 1, 3): L(
            "narrateur|Nina glisse le bouton sous la couverture du livre.",
            "narrateur|Une plume rousse marque la page du bateau.",
            "enfant-f|C'est son ticket, à la poule.",
            "papa|On le sort pour le manteau ?",
            "enfant-f|Oui, après la plume.",
            "maman|La pomme a un bec, sur la peau.",
            "narrateur|Elle pousse le rouge dans le trou.",
            "narrateur|Le livre se ferme sur une virgule de fil, oubliée.",
        ),
        (2, 2, 1): L(
            "narrateur|Nina coud près de la fenêtre de la classe.",
            "narrateur|Une perle de yaourt et un poil gris tiennent au fil.",
            "papa|Tu vois le rond, là ?",
            "enfant-f|Oui, il attendait.",
            "maman|La page a une goutte sèche, en coin.",
            "narrateur|Le dernier point serre la virgule.",
            "narrateur|Le manteau ne baille plus, contre la vitre.",
        ),
        (2, 2, 2): L(
            "narrateur|Nina pose le bouton sur le banc, à côté du livre.",
            "narrateur|L'empreinte du chien croise un croissant de yaourt.",
            "enfant-f|Deux virgules.",
            "papa|Laquelle est la nôtre ?",
            "enfant-f|Le fil blanc.",
            "maman|La reliure sent le lait.",
            "narrateur|Elle enfile le rouge, le livre fermé sur les genoux.",
            "narrateur|Le banc garde les deux marques, un moment.",
        ),
        (2, 2, 3): L(
            "narrateur|Nina range bouton et livre dans le cartable.",
            "narrateur|Une plume colle à la perle de yaourt.",
            "enfant-f|Ils voyagent ensemble.",
            "papa|On coud ce soir ?",
            "enfant-f|Oui, le fil est assez long.",
            "maman|La page du bateau est sèche ?",
            "enfant-f|Sèche.",
            "narrateur|Le cartable se ferme sur la virgule blanche.",
        ),
        (2, 3, 1): L(
            "narrateur|Nina recoud au coin du crochet, de retour.",
            "narrateur|Une miette de pain et un poil de chat partagent le fil.",
            "papa|Le trou est juste ?",
            "enfant-f|Juste.",
            "maman|Le livre sent le pain chaud, un peu.",
            "narrateur|Le tic du radiateur guide le dernier point.",
            "narrateur|Le manteau ferme, le crochet reste vide.",
        ),
        (2, 3, 2): L(
            "narrateur|Nina s'assoit sur la marche du bas, le livre ouvert.",
            "narrateur|Le bouton a une croûte, et un poil de chien.",
            "enfant-f|Il a voyagé dans la gueule.",
            "papa|On le lave ?",
            "enfant-f|Un peu d'eau, puis le trou.",
            "maman|Une miette dort dans le pli du bateau.",
            "narrateur|Elle pousse le rouge, le fil en virgule.",
            "narrateur|La marche du bas garde une miette, oubliée.",
        ),
        (2, 3, 3): L(
            "narrateur|Nina glisse le bouton dans le manteau, dehors.",
            "narrateur|Une plume et une miette tiennent au fil.",
            "enfant-f|Ça raconte la poule, et le pain.",
            "papa|Le livre rentre ?",
            "enfant-f|Oui, le bateau a fini.",
            "maman|Le trou est plein, maintenant ?",
            "enfant-f|Plein.",
            "narrateur|La virgule de fil dépasse, comme un sourire.",
        ),
        (3, 1, 1): L(
            "narrateur|Nina pose le bouton dans la petite tasse, une dernière fois.",
            "narrateur|Un poil de chat et un jus de pomme y brillent.",
            "enfant-f|Cerise vraie, maintenant.",
            "papa|On la coud, cette cerise ?",
            "enfant-f|Oui, le goûter est fini.",
            "maman|L'assiette a un rond de pomme.",
            "narrateur|Elle pousse le rouge dans le manteau.",
            "narrateur|La tasse reste vide, tiède, sur la marche.",
        ),
        (3, 1, 2): L(
            "narrateur|Nina essuie le bouton à la serviette de dînette.",
            "narrateur|Le museau du chien a mouillé la cerise.",
            "narrateur|La pomme a laissé un croissant, dans l'assiette.",
            "enfant-f|Deux ronds, un fil.",
            "papa|Lequel va au manteau ?",
            "enfant-f|Le rouge.",
            "maman|La tasse a un goût de chien, un peu.",
            "narrateur|Le manteau ferme sur la virgule de fil.",
        ),
        (3, 1, 3): L(
            "narrateur|Nina accroche le bouton au crochet de la cour.",
            "narrateur|Une plume pend dans la tasse, en dessous.",
            "enfant-f|La poule a payé sa visite.",
            "papa|On le remet après la plume ?",
            "enfant-f|Oui.",
            "maman|La pomme a un trou de bec, dans l'assiette.",
            "narrateur|Elle enfile le rouge, la tasse au soleil.",
            "narrateur|Le crochet de la cour reste vide, ensuite.",
        ),
        (3, 2, 1): L(
            "narrateur|Nina coud près de la dînette rangée.",
            "narrateur|Une perle de yaourt et un poil gris tiennent au fil.",
            "papa|La tasse est sèche ?",
            "enfant-f|Sèche.",
            "maman|Le rond du fond a disparu.",
            "narrateur|Le dernier point serre la virgule.",
            "narrateur|Le manteau ferme, la casserole de dînette se tait.",
        ),
        (3, 2, 2): L(
            "narrateur|Nina pose le bouton dans la soucoupe, sur le banc.",
            "narrateur|L'empreinte du chien croise une perle de yaourt.",
            "enfant-f|La soucoupe sert de nid.",
            "papa|On le prend, pour le trou ?",
            "enfant-f|Oui, le nid a fini.",
            "maman|La tasse sent le lait, et le chien.",
            "narrateur|Elle pousse le rouge, la soucoupe vide.",
            "narrateur|Le banc garde un croissant blanc, un moment.",
        ),
        (3, 2, 3): L(
            "narrateur|Nina range bouton et tasse dans le cartable.",
            "narrateur|Une plume colle à la perle de yaourt.",
            "enfant-f|La cerise voyage.",
            "papa|On coud ce soir ?",
            "enfant-f|Oui, le fil est long.",
            "maman|La dînette rentre aussi ?",
            "enfant-f|La tasse, oui.",
            "narrateur|La tasse cliquette une fois, puis plus rien.",
        ),
        (3, 3, 1): L(
            "narrateur|Nina recoud au coin du crochet, la casserole à côté.",
            "narrateur|Une miette et un poil de chat partagent le fil.",
            "papa|Le trou est juste ?",
            "enfant-f|Juste.",
            "maman|La dînette sent le pain, un peu.",
            "narrateur|Le tic du radiateur suit le dernier point.",
            "narrateur|La casserole de dînette reste tiède, vide.",
        ),
        (3, 3, 2): L(
            "narrateur|Nina s'assoit sur la marche du milieu, la casserole sur les genoux.",
            "narrateur|Le bouton a une croûte, et un poil de chien.",
            "enfant-f|Le gâteau a voyagé.",
            "papa|On le brosse ?",
            "enfant-f|Oui, puis le trou.",
            "maman|Une miette dort dans la casserole.",
            "narrateur|Elle pousse le rouge, le fil en virgule.",
            "narrateur|La marche du milieu garde une miette, oubliée.",
        ),
        (3, 3, 3): L(
            "narrateur|Nina glisse le bouton dans le manteau, dehors.",
            "narrateur|Une plume et une miette tiennent au fil.",
            "enfant-f|Ça raconte la poule, et le gâteau.",
            "papa|La dînette rentre ?",
            "enfant-f|Oui, la soupe pour de rire est finie.",
            "maman|Le trou est plein, maintenant ?",
            "enfant-f|Plein.",
            "narrateur|Une plume pique le col, tout léger.",
        ),
    }

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        put(f"{p}_T0002_P0000", t2_choice[a], "choice", "", None)
        extras[f"{p}_T0002_P0000"] = t3labs("une pomme", "un yaourt", "un morceau de pain")
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            snack_son = {1: "pomme", 2: "yaourt", 3: "pain"}[b]
            snack_emp = {1: "pomme", 2: "yaourt", 3: "pain"}[b]
            put(sp, t2_pass[(a, b)], "obstacle", snack_son, snack_emp)
            put(f"{sp}_T0003_P0000", t3_choice[b], "choice", "", None)
            extras[f"{sp}_T0003_P0000"] = t3labs("le chat", "le chien", "la poule")
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                ani_son = {1: "chat", 2: "chien", 3: "poule"}[c]
                ani_emp = {1: "virgule", 2: "virgule", 3: "virgule"}[c]
                put(leaf, t3_pass[(b, c)] + t1_echo[a], "resolution", ani_son, ani_emp)
                fin = f"{leaf}_F0001"
                put(fin, ends[(a, b, c)], "ending", "manteau,cour", "bouton")

    fin_texts = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                cid = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001"
                txt, _ = from_script(s[cid])
                fin_texts.append(txt)
    if len(set(fin_texts)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fin_texts))}")

    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in s]
    extra_ids = set(s) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        nc = make_chunk(c, s[cid], sons.get(cid, ""), 1.22, "medium")
        if cid in extras:
            nc.update(extras[cid])
        voice(nc, prof[cid], emph.get(cid), sons.get(cid, ""))
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = (
        "Nina veut remettre son bouton rouge au manteau avant la cour. "
        "Un fil blanc en pend, plié en virgule. Elle parle par-dessus Aniss : "
        "le bouton tombe. Cubes, livre ou dînette changent le premier jeu. "
        "Pomme, yaourt ou pain changent le goûter partagé. "
        "Chat, chien ou poule, dans la cour des trois marches, jouent avec le fil. "
        "Nina refuse de foncer, retrouve la virgule du crochet. "
        "Le manteau ferme, le fil porte une trace du chemin."
    )
    out["title"] = "Le bouton rouge de Nina"
    out["characters"] = "Nina, Aniss, papa, maman"
    out["setting"] = "classe au coin du crochet, puis la cour des trois marches"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in ("on va apprendre", "voici le geste", "l'histoire est finie", "bon travail", "maîtresse", "maitresse"):
        if bad in blob:
            raise SystemExit(f"reste interdit: {bad}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    nwords = sum(words(c["text"]) for c in out["chunks"])
    path_lens = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                ids = [
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
                path_lens.append(sum(words(by[i]["text"]) for i in ids))
    relecture = f"""# TREE-COL-009 — Le bouton rouge de Nina

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse
Nina veut remettre son bouton rouge au manteau avant d'aller dans la cour des trois marches. Un fil blanc en pend, plié en virgule — l'indice du crochet. Aniss veut commencer sa route en même temps. Nina parle par-dessus : le bouton tombe sous le radiateur. Cubes, livre ou dînette changent le premier jeu. Pomme, yaourt ou pain changent le goûter. Chat, chien ou poule jouent avec le fil. Nina refuse de foncer, retrouve la virgule. Vingt-sept fins ramènent le bouton au manteau, chacune avec une trace du chemin.

## Vécu
Tours de parole : envie de couper, chute du bouton, retenue, écoute d'Aniss, plaisir d'être entendue. La leçon se voit (tour qui penche, page coincée, tasse tapée, animal qui part). Elle n'est pas dite. Papa s'accroupit. Maman pose des questions. Un merci vécu.

## Vu et corrigé
- N3 ≤ 16 mots/phrase. Troupe D16 : Nina, Aniss, papa, maman. Pas de maîtresse.
- Ouverture par le trou vide du manteau, pas un gabarit v2.
- Indice unique : virgule de fil, payée au climax et à la fin.
- T1/T2/T3 changent l'action (jeu, goûter, ruse animale).
- 27 fins textuellement distinctes.
- TTS par fonction (opening/choice/clue/confirm/action/obstacle/resolution/ending).
- `en ce moment`, questions d'adulte, un merci vécu.
- Pas apply. Pas git. Pas audio.

## Contrôles
- 86 chunks, 27 chemins
- {nwords} mots au total
- {min(path_lens)} à {max(path_lens)} mots par chemin, moyenne {sum(path_lens)//len(path_lens)}
- `check()` OK

## Non vérifié
Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
"""
    (folder / "RELECTURE.md").write_text(relecture, encoding="utf-8")
    print(f"OK {SID} {nwords} mots  chemins {min(path_lens)}-{max(path_lens)}")


if __name__ == "__main__":
    main()
