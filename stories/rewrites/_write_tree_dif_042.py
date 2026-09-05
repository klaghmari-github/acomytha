#!/usr/bin/env python3
"""TREE-DIF-042 — Le cacao de Nina, trop haut sur l'étagère (F-NAR-019, N3, TTS)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-DIF-042"
LIM = LIMITS["N3"]
TITLE = "Le cacao de Nina, trop haut sur l'étagère"
FIL = (
    "La casserole fait tic. Nina veut deux tasses de cacao, avant la peau du lait. "
    "Le bidon penche son capuchon, trop haut. Victorino est plus grand, sans se presser. "
    "Ils emportent le bidon, le fouet et les deux tasses. "
    "À l'étagère, au frigo, sous la table : neuf façons. "
    "Le capuchon penche jusqu'à la fin."
)
CHARS = "Nina, Victorino, papa, maman"
SETTING = "cuisine : étagère, frigo, sous la table"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="capuchon",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_capuchon_penche_trop_haut; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_vient_d_arriver; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=le_cacao_voyage_avec_eux; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=elle_veut_le_bidon_tout_de_suite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=la_première_idée_rate; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis="capuchon",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_capuchon_guide_sans_foncer; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="capuchon",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_capuchon_penche_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
    ),
}

TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "mission accomplie",
    "j'ai compris",
    "bon travail",
    "bravo tu as",
    "la première",
    "la deuxième",
    "la troisième",
    "aujourd'hui",
    "tailles différentes",
    "plus petit ou plus grand",
)


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic « {tic} »: {ph}")
        for tic in ("encore", "déjà", "deja", "tout doux", "tout calme"):
            if tic in low:
                raise SystemExit(f"tic corpus « {tic} »: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"puces « {tok} »: {ph}")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""
        out.append(f"{role}|{ph}")
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emph = m.get("emphasis")
    if emph:
        e = esc(emph)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emph = m.get("emphasis")
    if emph:
        body = body.replace(emph, f"<emphasis>{emph}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    tail = " [long-pause]" if m["pause"] >= 800 else (" [pause]" if m["pause"] >= 400 else "")
    return (body + tail).strip()


def voice(text: str, profile: str, extra: dict | None = None) -> dict:
    m = dict(PROFILES[profile])
    extra = extra or {}
    if extra.get("emphasis") is not None:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    pause_before = extra.get("pause_before", 0)
    return {
        "text_ssml": ssml(text, m),
        "text_xai_tags": xai(text, m),
        "rate_wpm": m["wpm"],
        "rate_label": m["rate"],
        "speed_xai": m["speed"],
        "length_scale_piper": m["piper"],
        "pitch_label": m["pitch"],
        "pitch_ssml": m["pitch_ssml"],
        "pitch_xai_tag": m["pitch_tag"],
        "volume_label": m["volume"],
        "volume_db": m["db"],
        "emphasis_words": m["emphasis"] or "",
        "pause_before_ms": pause_before,
        "pause_after_ms": m["pause"],
        "pause_sentence_ms": m["sentence"],
        "style_energy": m["energy"],
        "style_contour": m["contour"],
        "noise_scale_piper": m["noise"],
        "kokoro_speed": m["speed"],
        "melo_speed": m["speed"],
        "espeak_amp": 82 if m["volume"] == "soft" else 100,
        "espeak_pitch": 42 if m["pitch"] == "low" else 50,
        "espeak_word_gap": 12 if m["rate"] == "slow" else 8,
        "notes": m["note"],
        "night_policy": "play",
        "locale": "fr-FR",
        "voice_id": "fr_FR-siwis-medium",
    }


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


T1 = {
    1: {
        "lab": "le bidon de cacao",
        "ans": "hanche",
        "acc": "hanche | la hanche | contre la hanche | sa hanche",
        "retry": "Le bidon est contre la hanche.",
        "emph": "bidon",
        "sons": "metal,poudre",
    },
    2: {
        "lab": "le fouet",
        "ans": "poche",
        "acc": "poche | la poche | dans la poche | sa poche",
        "retry": "Le fouet est dans la poche.",
        "emph": "fouet",
        "sons": "tiroir,clic",
    },
    3: {
        "lab": "les deux tasses",
        "ans": "plateau",
        "acc": "plateau | le plateau | sur le plateau | le bois",
        "retry": "Les tasses sont sur le plateau.",
        "emph": "tasses",
        "sons": "porcelaine,plateau",
    },
}

T3_LABS = {
    1: ("les bras de Victorino", "le tabouret de Nina", "le torchon ensemble"),
    2: ("la poignée haute", "le bac du bas", "le tabouret à deux"),
    3: ("le passage de Nina", "écarter la chaise", "un dessous un dessus"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina lève les bras vers le bidon de cacao.",
            "enfant-f|Je le prends !",
            "narrateur|Ses doigts frôlent le métal, trop loin.",
            "narrateur|Le capuchon penche, un peu plus.",
            "narrateur|Un nuage de poudre tombe, minuscule.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Nina se plie.",
            "copain|Attends.",
            "narrateur|Victorino se hausse, sans se presser.",
            "narrateur|Il descend le bidon, vers sa hanche à elle.",
            "maman|Garde-le contre ta hanche, bien droit.",
            "papa|Le fouet, dans la poche, ensuite.",
            "narrateur|Victorino pose les deux tasses sur le plateau.",
            "enfant-f|On a tout, pour deux.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina ouvre le tiroir, à sa hauteur.",
            "enfant-f|Le fouet, d'abord.",
            "narrateur|Les fils râpent sa paume, un peu.",
            "papa|Glisse-le dans ta poche.",
            "narrateur|Un clic de métal, tout petit.",
            "enfant-f|Victorino, le bidon, maintenant.",
            "narrateur|Elle saute vers l'étagère, trop vite.",
            "narrateur|Le capuchon penche, et la poudre tousse.",
            "copain|Pas comme ça.",
            "narrateur|Il tend le bidon, sans se presser.",
            "maman|Contre la hanche, Nina.",
            "narrateur|Victorino pose les deux tasses sur le plateau.",
            "enfant-f|Le fouet est prêt, dans ma poche.",
            "papa|Vous avez les trois, alors.",
        )
    return L(
        "narrateur|Nina soulève les deux tasses, l'une petite.",
        "enfant-f|La grande est pour toi.",
        "maman|Pose-les sur le plateau, bien droit.",
        "narrateur|La porcelaine fait un petit choc.",
        "papa|Le bidon et le fouet, avec vous.",
        "enfant-f|J'attrape le bidon !",
        "narrateur|Ses bras manquent le capuchon penché.",
        "copain|Moi j'y arrive, lentement.",
        "narrateur|Il pose le bidon contre sa hanche à elle.",
        "narrateur|Le fouet glisse dans la poche, clic.",
        "enfant-f|Je te garde la grande tasse.",
        "copain|D'accord.",
        "papa|Les tasses d'abord, elles sont prêtes.",
        "maman|Rien ne reste près de la fenêtre.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina a mis le bidon de cacao contre la hanche.",
            "maman|C'est où, maintenant ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina a glissé le fouet dans la poche.",
            "papa|C'est où, maintenant ?",
        )
    return L(
        "narrateur|Nina a posé les deux tasses sur le plateau.",
        "maman|C'est où, maintenant ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-f|Contre la hanche.",
            "maman|Oui.",
            "copain|Il est froid.",
            "enfant-f|Il va chauffer dans le lait.",
            "narrateur|Victorino a les genoux plus hauts que Nina.",
            "narrateur|Ses mains touchent le bord du plan.",
            "papa|On reste dans la cuisine ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le capuchon penche, contre la robe.",
        )
    if t1 == 2:
        return L(
            "enfant-f|Dans la poche.",
            "papa|Oui.",
            "copain|J'entends le clic.",
            "enfant-f|Ne le sors pas.",
            "narrateur|Victorino se baisse, trop long, trop vite.",
            "narrateur|Une mèche saute au-dessus du pichet.",
            "maman|Vos mains, au-dessus du plateau ?",
            "copain|Oui, maman.",
            "narrateur|Le capuchon penche, près du fouet.",
        )
    return L(
        "enfant-f|Sur le plateau.",
        "maman|Oui.",
        "copain|La grande est à moi ?",
        "enfant-f|Oui, la petite est à moi.",
        "narrateur|Le pull de Victorino laisse ses poignets nus.",
        "narrateur|Nina, plus courte, tient le plateau des deux mains.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
        "narrateur|Le capuchon penche, au-dessus des tasses.",
    )


def t2_question(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le bidon tape la hanche, froid.",
            "narrateur|L'étagère reste trop haute.",
            "narrateur|Le frigo garde son lait, trop loin.",
            "narrateur|Sous la table, l'ombre est basse.",
            "papa|Nina, vous mélangez où ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le fouet frotte la poche, un peu rêche.",
            "narrateur|L'étagère, le frigo, ou sous la table.",
            "maman|Vous mélangez où, Nina ?",
        )
    return L(
        "narrateur|Les tasses s'entrechoquent, sur le plateau.",
        "narrateur|L'étagère, le frigo, ou sous la table.",
        "papa|Vous mélangez où, Nina ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    table = {
        (1, 1): L(
            "narrateur|Nina pose le bidon sur le plan, sous l'étagère.",
            "enfant-f|On mélange dans le grand bol, là-haut.",
            "copain|Moi je vois le fond.",
            "narrateur|Nina saute, d'un coup.",
            "narrateur|Ses doigts manquent le bord.",
            "narrateur|La poudre tombe, à côté de ses yeux.",
            "enfant-f|Je ne vois plus rien.",
            "narrateur|Son sourire disparaît.",
            "narrateur|L'envie et la peur se poussent, dans son ventre.",
            "copain|Je mélange en haut, moi.",
            "enfant-f|Non, en bas, avec moi.",
            "narrateur|Victorino se tait, un moment.",
            "papa|Je me baisse, pour voir comme vous.",
            "papa|Vous faites comment, tous les deux ?",
        ),
        (2, 1): L(
            "narrateur|Nina pose le fouet sur le plan, trop haut.",
            "enfant-f|Je fouette dans le grand bol !",
            "copain|Les fils, je les vois, moi.",
            "narrateur|Elle se hisse sur la pointe.",
            "narrateur|Le fouet disparaît derrière le bol.",
            "enfant-f|Il est où ?",
            "narrateur|Un cliquetis, trop loin pour elle.",
            "narrateur|Son sourire tombe.",
            "narrateur|Ça serre, juste sous la gorge.",
            "copain|Je fouette en haut.",
            "enfant-f|Je veux le sentir, moi.",
            "maman|Je m'accroupis, à votre hauteur.",
            "papa|Vous trouvez comment, alors ?",
        ),
        (3, 1): L(
            "narrateur|Nina pose le plateau sur le plan, sous l'étagère.",
            "enfant-f|Les tasses, dans le bol, là-haut.",
            "copain|Elles n'arrivent pas, trop basses.",
            "narrateur|Elle pousse le plateau vers le haut.",
            "narrateur|Une tasse penche, puis se rattrape.",
            "enfant-f|Attention !",
            "narrateur|Le sourire de Nina s'efface.",
            "narrateur|Ses mains tremblent, un peu.",
            "copain|Moi je les mets en haut.",
            "enfant-f|Pas sans moi.",
            "narrateur|Il attend, les bras le long du corps.",
            "papa|Je me baisse, face au bois.",
            "maman|Vous faites comment, tous les deux ?",
        ),
        (1, 2): L(
            "narrateur|Nina tape le bidon contre la porte, toc.",
            "enfant-f|Le lait, il est où ?",
            "maman|Dans le frigo, il brûlait trop.",
            "copain|Je vois le beurre, tout haut.",
            "enfant-f|Je veux le lait, pas le beurre.",
            "narrateur|Elle tire le bas de la porte.",
            "narrateur|La porte s'ouvre, puis claque.",
            "narrateur|La poignée reste trop loin pour Nina.",
            "enfant-f|Aïe.",
            "narrateur|Son sourire n'est plus là.",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "papa|Je m'accroupis, près du joint.",
            "papa|Vous ouvrez comment, tous les deux ?",
        ),
        (2, 2): L(
            "narrateur|Nina tape le fouet contre la porte, toc.",
            "enfant-f|On a besoin de lait froid.",
            "copain|Le beurre est plus près, en haut.",
            "enfant-f|Le lait, Victorino.",
            "narrateur|Elle accroche le fouet au loquet.",
            "narrateur|Les fils glissent, sans ouvrir.",
            "copain|Ça ne tient pas.",
            "narrateur|Un souffle froid lève, puis retombe.",
            "narrateur|Nina serre les dents.",
            "narrateur|Ça serre, dans le ventre.",
            "maman|Je me baisse, face à la poignée.",
            "papa|Vous trouvez, tous les deux ?",
        ),
        (3, 2): L(
            "narrateur|Nina tape le plateau contre la porte, toc.",
            "enfant-f|Le lait manque, pour deux tasses.",
            "copain|Je prends le beurre, moi.",
            "enfant-f|Non, le lait.",
            "narrateur|Les tasses n'ouvrent rien, trop basses.",
            "narrateur|La porcelaine cliquette, contre le joint.",
            "enfant-f|Elles vont tomber.",
            "narrateur|Elle recule le plateau, trop vite.",
            "narrateur|Son sourire a disparu.",
            "narrateur|Deux envies, au même instant.",
            "papa|Je m'accroupis, à votre hauteur.",
            "maman|Vous ouvrez comment, alors ?",
        ),
        (1, 3): L(
            "narrateur|Nina glisse le bidon sous la table, tout bas.",
            "enfant-f|On goûte ici, comme une grotte.",
            "copain|Moi je veux le plan, en haut.",
            "enfant-f|Non, ici.",
            "narrateur|Victorino force, trop large.",
            "narrateur|Ses épaules butent contre le bois.",
            "copain|Je rentre pas.",
            "narrateur|Le cacao prend une miette, sur les carreaux.",
            "enfant-f|Oh, le bidon.",
            "narrateur|Le sourire de Nina s'en va.",
            "narrateur|Elle serre le capuchon penché, trop fort.",
            "maman|Je me baisse, sous le bord.",
            "papa|Vous goûtez comment, tous les deux ?",
        ),
        (2, 3): L(
            "narrateur|Nina glisse le fouet sous la table, tout bas.",
            "enfant-f|On fouette ici, dans l'ombre.",
            "copain|L'ombre est trop petite, pour moi.",
            "enfant-f|Essaie.",
            "narrateur|Il pousse, d'un coup.",
            "narrateur|Le fouet roule, puis s'arrête contre un pied.",
            "copain|Aïe, l'épaule.",
            "narrateur|Nina ne rit plus.",
            "narrateur|Ça serre, sous les côtes.",
            "copain|Je reste dehors, alors.",
            "enfant-f|Sans toi, non.",
            "papa|Je m'accroupis, près des chaises.",
            "maman|Vous trouvez comment, alors ?",
        ),
        (3, 3): L(
            "narrateur|Nina glisse le plateau sous la table, tout bas.",
            "enfant-f|Les tasses, dans la grotte.",
            "copain|Je veux trinquer sur le bois, moi.",
            "enfant-f|En dessous, Victorino.",
            "narrateur|Il se plie, trop vite.",
            "narrateur|Une tasse cliquette, trop près d'une chaise.",
            "enfant-f|Stop.",
            "narrateur|Le plateau attend au bord, un peu seul.",
            "narrateur|Son sourire n'est plus là.",
            "narrateur|Deux projets, coincés au même moment.",
            "maman|Je me baisse, face à l'ombre.",
            "papa|Vous faites comment, tous les deux ?",
        ),
    }
    return table[(t1, t2)]


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'étagère attend, trop haute.",
            "papa|Les bras, le tabouret, ou le torchon ensemble ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La poignée attend, trop loin.",
            "maman|La poignée, le bac, ou le tabouret ?",
        )
    return L(
        "narrateur|L'ombre sous la table attend.",
        "papa|Le passage, écarter, ou un dessous un dessus ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "enfant-f|Attends, je ne fonce pas.",
            "narrateur|Nina regarde le bidon, sans bouger.",
            "narrateur|Le capuchon penche, comme au départ.",
            "enfant-f|C'est le nôtre, je le reconnais.",
            "narrateur|Victorino se tait.",
            "copain|D'accord, je tourne, moi.",
            "narrateur|Il mélange dans le bol, assez haut.",
            "narrateur|Nina verse d'en bas, par le capuchon penché.",
            "enfant-f|Je tiens le pichet.",
            "papa|Tes bras allaient jusque-là.",
            "copain|Goûte, Nina.",
            "enfant-f|Il est à nous.",
        ),
        (1, 1, 2): L(
            "enfant-f|Pas de saut, le tabouret.",
            "papa|Tiens le bois, Nina.",
            "narrateur|Elle monte, le nez au bord du bol.",
            "narrateur|Le capuchon penche, à hauteur d'yeux.",
            "enfant-f|Je le vois, de travers, comme tout à l'heure.",
            "copain|Moi je verse le lait, tout près.",
            "narrateur|Victorino tient le pichet, au-dessus.",
            "narrateur|La poudre glisse vers le fond.",
            "copain|Tu vois, maintenant.",
            "maman|Vous le partagez.",
            "narrateur|Le bidon attend au bord, plein d'ombre.",
            "enfant-f|On a failli le rater.",
        ),
        (1, 1, 3): L(
            "enfant-f|On tire le bol, sans sauter.",
            "copain|Moi aussi, je tire.",
            "narrateur|Victorino enroule un torchon, tout haut.",
            "narrateur|Nina tire l'autre bout, plus bas.",
            "narrateur|Le capuchon penche vers eux, comme un signe.",
            "enfant-f|C'est lui, on tire jusque-là.",
            "narrateur|Le bidon glisse avec le torchon, lentement.",
            "papa|Le bol est venu vers vous.",
            "copain|On le tient.",
            "enfant-f|Il fume.",
            "maman|Vos cheveux sentent le linge chaud.",
            "narrateur|Le capuchon penche, pris dans le tissu.",
        ),
        (1, 2, 1): L(
            "enfant-f|Stop, on ouvre pas n'importe comment.",
            "narrateur|Elle plaque le bidon contre la porte.",
            "narrateur|Le capuchon penche, dans le rai froid.",
            "enfant-f|Le lait, pas le beurre.",
            "copain|Je me hausse, alors.",
            "narrateur|Les doigts de Victorino touchent la poignée.",
            "copain|Elle bouge.",
            "narrateur|La bouteille de lait penche, puis avance.",
            "narrateur|Victorino pose le bidon contre la porte.",
            "papa|Tes doigts allaient assez loin.",
            "maman|Nina tenait bien le bas.",
            "copain|Le lait est à nous.",
        ),
        (1, 2, 2): L(
            "enfant-f|Je n'ouvre plus le bas, j'ouvre le bac.",
            "copain|Oui, lentement.",
            "narrateur|Nina pose le bidon près du bac.",
            "narrateur|Le capuchon penche, dans le blanc du tiroir.",
            "enfant-f|Le lait est là, en bas.",
            "narrateur|Papa tient la porte, bien ferme.",
            "narrateur|Nina tire le bac, Victorino veille.",
            "copain|Il est froid.",
            "maman|Vous avez regardé ensemble.",
            "papa|Le bac est resté doux.",
            "enfant-f|On a failli chercher trop haut.",
            "narrateur|Le capuchon penche, face à la bouteille.",
        ),
        (1, 2, 3): L(
            "enfant-f|Reste en haut, Victorino.",
            "copain|Je tends, d'ici.",
            "narrateur|Victorino tend le bidon, bras tout longs.",
            "narrateur|Le capuchon penche vers le loquet, comme une clé.",
            "enfant-f|On partage le tabouret.",
            "narrateur|Le tabouret prend Nina, puis lui.",
            "narrateur|Victorino fait basculer le loquet, sans forcer.",
            "enfant-f|Je tiens la bouteille.",
            "papa|Chacun a fait sa part.",
            "copain|Elle sent le froid.",
            "maman|Vos bras n'avaient pas la même longueur.",
            "narrateur|Le capuchon penche, contre le joint.",
        ),
        (1, 3, 1): L(
            "enfant-f|Je passe, toi tu restes.",
            "narrateur|Nina rampe, toute petite, sous la table.",
            "copain|Je fouette ici, dehors.",
            "narrateur|Elle pousse le bidon sous le bois.",
            "narrateur|Le capuchon penche, comme une petite lanterne.",
            "enfant-f|Je le reconnais, de travers.",
            "narrateur|Ses doigts trouvent la petite tasse.",
            "enfant-f|Je la tiens.",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Une grotte de vapeur s'ouvre, à eux.",
            "copain|Je te verse, d'ici.",
            "enfant-f|Elle est à nous.",
        ),
        (1, 3, 2): L(
            "enfant-f|On écarte la chaise, sans forcer.",
            "copain|Moi aussi, j'écarte.",
            "narrateur|Victorino tire la chaise, tout haut.",
            "narrateur|Nina se glisse, pendant l'ouverture.",
            "narrateur|Le bidon avance vers le jour.",
            "narrateur|Le capuchon penche, et cogne le pied, toc.",
            "enfant-f|C'est lui, il n'est pas tombé.",
            "papa|La place est venue vers vous.",
            "copain|Je rentre, de côté.",
            "enfant-f|On y est, tous les deux.",
            "maman|Vos cheveux sentent le bois chaud.",
            "narrateur|Le capuchon penche, dans la lumière basse.",
        ),
        (1, 3, 3): L(
            "enfant-f|Papa, écarte un peu ?",
            "papa|Je fais un chemin, lentement.",
            "narrateur|Une chaise s'ouvre, comme une aile.",
            "narrateur|Nina rentre, Victorino reste dehors.",
            "narrateur|Le bidon devient un nid, contre le bois.",
            "narrateur|Le capuchon penche, entre le dessous et le dessus.",
            "copain|On trinque à travers ?",
            "enfant-f|Oui, petite tasse, grande tasse.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux voix tiennent le même secret.",
            "enfant-f|Le capuchon, je le vois, de travers.",
            "copain|Moi aussi, d'en haut.",
        ),
        (2, 1, 1): L(
            "enfant-f|J'arrête de me hisser, regarde.",
            "narrateur|Le fouet attend au bord, un peu rêche.",
            "narrateur|Le capuchon penche, juste à côté.",
            "enfant-f|C'est notre bidon, tu mélanges, toi.",
            "copain|Je tourne, alors.",
            "narrateur|Victorino fouette dans le bol, assez haut.",
            "narrateur|Nina tend le fouet, bras tout courts, puis lâche.",
            "enfant-f|Je verse le lait, d'en bas.",
            "papa|Tes bras allaient assez loin.",
            "copain|Ça mousse, un peu.",
            "maman|Le clic du fouet est revenu.",
            "enfant-f|On a failli le perdre derrière le bol.",
        ),
        (2, 1, 2): L(
            "enfant-f|Je monte, sans sauter.",
            "papa|Tiens le bois, Nina.",
            "narrateur|Nina se hausse, le nez au bord du bol.",
            "narrateur|Le capuchon penche, et le fouet réapparaît.",
            "enfant-f|Les fils, je les vois.",
            "copain|Moi je verse, tout près.",
            "narrateur|Victorino tient le pichet, au-dessus.",
            "narrateur|La poudre glisse, le fouet tourne.",
            "copain|Tu vois, maintenant.",
            "maman|Vous le partagez.",
            "narrateur|Le fouet attend au bord, un peu rêche.",
            "enfant-f|Le capuchon m'a guidée.",
        ),
        (2, 1, 3): L(
            "enfant-f|On tire le bol, avec le torchon.",
            "copain|Moi aussi, je tire.",
            "narrateur|Victorino enroule un torchon, tout haut.",
            "narrateur|Nina tire l'autre bout, plus bas.",
            "narrateur|Le fouet glisse avec le torchon, clic.",
            "narrateur|Le capuchon penche vers le linge, comme un crochet.",
            "enfant-f|On s'arrête là, c'est lui.",
            "papa|Le bol est venu vers vous.",
            "copain|On le tient.",
            "enfant-f|Il fume.",
            "maman|Vos cheveux sentent le linge chaud.",
            "narrateur|Un fil du fouet reste pris, un instant.",
        ),
        (2, 2, 1): L(
            "enfant-f|On n'accroche plus le loquet, tu ouvres.",
            "copain|Je me hausse.",
            "narrateur|Nina tient les tasses, d'en bas.",
            "narrateur|Le fouet reste dans la poche, clic.",
            "narrateur|Le capuchon penche, dans le rai du frigo.",
            "enfant-f|Le lait, là, pas le beurre.",
            "copain|Elle bouge, la poignée.",
            "narrateur|La bouteille penche, puis avance.",
            "narrateur|Victorino pose le fouet contre la porte.",
            "papa|Tes doigts allaient assez loin.",
            "maman|Nina tenait bien le bas.",
            "copain|Le lait est à nous.",
        ),
        (2, 2, 2): L(
            "enfant-f|Le bac du bas, pas la poignée.",
            "copain|Oui, lentement.",
            "narrateur|Nina pose le fouet près du bac.",
            "narrateur|Le capuchon penche, dans le blanc froid.",
            "enfant-f|Le lait est là.",
            "narrateur|Papa tient la porte, bien ferme.",
            "narrateur|Nina tire le bac, Victorino veille.",
            "copain|Il est froid.",
            "maman|Vous avez regardé ensemble.",
            "papa|Le bac est resté doux.",
            "enfant-f|Le fouet n'a pas servi de clé.",
            "narrateur|Le capuchon penche, face au lait.",
        ),
        (2, 2, 3): L(
            "enfant-f|Reste en haut, je tiens le fouet.",
            "copain|Je tends, d'ici.",
            "narrateur|Victorino tend le fouet, bras tout longs.",
            "narrateur|Le capuchon penche vers le loquet.",
            "enfant-f|Tabouret à deux, alors.",
            "narrateur|Le tabouret prend Nina, puis lui.",
            "narrateur|Victorino fait basculer le loquet, sans forcer.",
            "enfant-f|Je tiens la bouteille.",
            "papa|Chacun a fait sa part.",
            "copain|Elle sent le froid.",
            "maman|Vos bras n'avaient pas la même longueur.",
            "narrateur|Le clic du fouet se tait, contre le joint.",
        ),
        (2, 3, 1): L(
            "enfant-f|Je passe, toi tu fouettes dehors.",
            "narrateur|Nina rampe, toute petite, sous la table.",
            "copain|Je fouette ici, oui.",
            "narrateur|Elle glisse le fouet sous le bois, puis le reprend.",
            "narrateur|Le capuchon penche, comme une lanterne ronde.",
            "enfant-f|Je le vois, de travers.",
            "narrateur|Ses doigts trouvent la petite tasse.",
            "enfant-f|Je la tiens.",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Une grotte de vapeur s'ouvre, à eux.",
            "copain|Je te verse, d'ici.",
            "enfant-f|Le fouet a fait sa part, dehors.",
        ),
        (2, 3, 2): L(
            "enfant-f|On écarte la chaise, le fouet attend.",
            "copain|Moi aussi, j'écarte.",
            "narrateur|Victorino tire la chaise, tout haut.",
            "narrateur|Nina se glisse, pendant l'ouverture.",
            "narrateur|Le fouet avance, un clic, vers le jour.",
            "narrateur|Le capuchon penche, et le clic s'arrête.",
            "enfant-f|C'est lui, on s'arrête.",
            "papa|La place est venue vers vous.",
            "copain|Je rentre, de côté.",
            "enfant-f|On y est, tous les deux.",
            "maman|Vos cheveux sentent le bois chaud.",
            "narrateur|Un fil du fouet touche le pied de chaise.",
        ),
        (2, 3, 3): L(
            "enfant-f|Papa, écarte un peu ?",
            "papa|Je fais un chemin, lentement.",
            "narrateur|Une chaise s'ouvre, comme une aile.",
            "narrateur|Nina rentre, Victorino reste dehors.",
            "narrateur|Le fouet devient un nid, contre le bois.",
            "narrateur|Le capuchon penche, entre deux hauteurs.",
            "copain|On trinque à travers ?",
            "enfant-f|Oui, toi tu fouettes, moi je tiens.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux voix tiennent le même secret.",
            "enfant-f|Le capuchon, je le vois.",
            "copain|Le fouet, je l'entends, d'en haut.",
        ),
        (3, 1, 1): L(
            "enfant-f|Je ne pousse plus le plateau, toi tu mélanges.",
            "narrateur|Nina pousse le plateau, tout près, puis s'arrête.",
            "narrateur|Le capuchon penche, au-dessus des deux tasses.",
            "enfant-f|C'est notre bidon, je le reconnais.",
            "copain|Je tourne, alors.",
            "narrateur|Victorino mélange dans le bol, assez haut.",
            "narrateur|Nina verse dans la petite tasse, d'en bas.",
            "enfant-f|La grande, je te la tends.",
            "papa|Tes bras allaient jusque-là.",
            "copain|Goûte, Nina.",
            "maman|Deux tasses, deux hauteurs.",
            "enfant-f|On a failli les faire tomber.",
        ),
        (3, 1, 2): L(
            "enfant-f|Je monte avec le plateau, sans sauter.",
            "papa|Tiens le bois, Nina.",
            "narrateur|Elle se hausse, le nez au bord du bol.",
            "narrateur|Le capuchon penche, entre les deux tasses.",
            "enfant-f|Je les vois, et lui aussi.",
            "copain|Moi je verse le lait, tout près.",
            "narrateur|Victorino tient le pichet, au-dessus.",
            "narrateur|La poudre glisse vers le fond.",
            "copain|Tu vois, maintenant.",
            "maman|Vous le partagez.",
            "narrateur|Le plateau attend au bord, un peu chaud.",
            "enfant-f|Le capuchon m'a dit : c'est ici.",
        ),
        (3, 1, 3): L(
            "enfant-f|On tire le bol, pas les tasses.",
            "copain|Moi aussi, je tire.",
            "narrateur|Victorino enroule un torchon, tout haut.",
            "narrateur|Nina tire l'autre bout, plus bas.",
            "narrateur|Le plateau glisse avec le linge, toc.",
            "narrateur|Le capuchon penche vers le tissu.",
            "enfant-f|On s'arrête, les tasses tiennent.",
            "papa|Le bol est venu vers vous.",
            "copain|On le tient.",
            "enfant-f|Il fume.",
            "maman|Vos cheveux sentent le linge chaud.",
            "narrateur|La petite tasse a un halo de vapeur.",
        ),
        (3, 2, 1): L(
            "enfant-f|Je tiens les tasses, tu ouvres, toi.",
            "copain|Je me hausse.",
            "narrateur|Les doigts de Victorino touchent la poignée.",
            "narrateur|Nina tient le plateau, d'en bas.",
            "narrateur|Le capuchon penche, dans le rai froid.",
            "enfant-f|Le lait, pour les deux tasses.",
            "copain|Elle bouge.",
            "narrateur|La bouteille penche, puis avance.",
            "narrateur|Victorino pose le plateau contre le joint.",
            "papa|Tes doigts allaient assez loin.",
            "maman|Nina tenait bien le bas.",
            "copain|Le lait est à nous.",
        ),
        (3, 2, 2): L(
            "enfant-f|J'ouvre le bac du bas, les tasses attendent.",
            "copain|Oui, lentement.",
            "narrateur|Nina pousse le plateau, tout près.",
            "narrateur|Le capuchon penche, dans le blanc du bac.",
            "enfant-f|Le lait est là.",
            "narrateur|Papa tient la porte, bien ferme.",
            "narrateur|Nina tire le bac, Victorino veille.",
            "copain|Il est froid.",
            "maman|Vous avez regardé ensemble.",
            "papa|Le bac est resté doux.",
            "enfant-f|Les tasses n'ont rien cassé.",
            "narrateur|Le capuchon penche, face aux deux porcelaines.",
        ),
        (3, 2, 3): L(
            "enfant-f|Reste en haut, je garde les tasses.",
            "copain|Je tends, d'ici.",
            "narrateur|Victorino pousse le plateau, tout près.",
            "narrateur|Le capuchon penche vers le loquet.",
            "enfant-f|Le tabouret, à deux.",
            "narrateur|Le tabouret prend Nina, puis lui.",
            "narrateur|Victorino fait basculer le loquet, sans forcer.",
            "enfant-f|Je tiens la bouteille.",
            "papa|Chacun a fait sa part.",
            "copain|Elle sent le froid.",
            "maman|Vos bras n'avaient pas la même longueur.",
            "narrateur|Les deux tasses se touchent, sans crier.",
        ),
        (3, 3, 1): L(
            "enfant-f|Je passe avec les tasses, toi tu restes.",
            "narrateur|Nina rampe, toute petite, sous la table.",
            "copain|Je fouette ici, dehors.",
            "narrateur|Elle pousse le plateau sous le bord.",
            "narrateur|Le capuchon penche, au-dessus de la petite tasse.",
            "enfant-f|Je la tiens.",
            "narrateur|Ses doigts trouvent le bord chaud.",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Une grotte de vapeur s'ouvre, à eux.",
            "copain|Je te verse, d'ici.",
            "enfant-f|Elle est à nous.",
            "maman|La grande tasse attend, dehors.",
        ),
        (3, 3, 2): L(
            "enfant-f|On écarte la chaise, le plateau d'abord.",
            "copain|Moi aussi, j'écarte.",
            "narrateur|Victorino tire la chaise, tout haut.",
            "narrateur|Nina se glisse, pendant l'ouverture.",
            "narrateur|Le plateau avance, toc, vers le jour.",
            "narrateur|Le capuchon penche, et la porcelaine se tait.",
            "enfant-f|C'est lui, les tasses tiennent.",
            "papa|La place est venue vers vous.",
            "copain|Je rentre, de côté.",
            "enfant-f|On y est, tous les deux.",
            "maman|Vos cheveux sentent le bois chaud.",
            "narrateur|La petite tasse a frôlé le pied, sans choir.",
        ),
        (3, 3, 3): L(
            "enfant-f|Papa, écarte un peu ?",
            "papa|Je fais un chemin, lentement.",
            "narrateur|Une chaise s'ouvre, comme une aile.",
            "narrateur|Nina rentre, Victorino reste dehors.",
            "narrateur|Le plateau devient un nid, contre le bois.",
            "narrateur|Le capuchon penche, entre deux tasses.",
            "copain|On trinque à travers ?",
            "enfant-f|Oui, petite tasse, grande tasse.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux voix tiennent le même secret.",
            "enfant-f|Je vois le capuchon, de dessous.",
            "copain|Moi je vois la grande tasse, de dessus.",
        ),
    }
    return table[(t1, t2, t3)]


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "narrateur|À l'étagère, le cacao sent le bois chaud.",
            "copain|Tu versais, moi je tournais.",
            "enfant-f|Tes bras ont vu le fond.",
            "papa|Vous l'avez, à deux.",
            "maman|Le bol dort sur le bois.",
            "narrateur|Le capuchon penche, avec une empreinte de cacao.",
            "enfant-f|On reste un peu.",
            "narrateur|Un rai brun s'endort sur les carreaux.",
            "narrateur|La casserole se tait, sur le feu.",
        ),
        (1, 1, 2): L(
            "narrateur|Sur le tabouret, deux têtes se posent.",
            "enfant-f|J'ai vu le fond, moi aussi.",
            "copain|Oui, tu étais assez haute.",
            "papa|Toi en bas, lui au-dessus, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            "narrateur|Le capuchon penche, une goutte de lait au bord.",
            "copain|Je reste un peu.",
            "narrateur|Une goutte reste collée au bol.",
            "narrateur|L'évier sent le cacao, rien qu'un peu.",
        ),
        (1, 1, 3): L(
            "narrateur|Le torchon redescend, lentement.",
            "copain|Le bol est venu vers nous.",
            "enfant-f|On a tiré, tous les deux.",
            "maman|Il n'était plus trop haut.",
            "papa|La poudre danse, dans l'air.",
            "narrateur|Le capuchon penche, pris d'un fil de linge.",
            "enfant-f|On souffle dessus.",
            "narrateur|Un rayon veille près des bols.",
            "narrateur|Le radiateur se tait, au fond.",
        ),
        (1, 2, 1): L(
            "narrateur|Au frigo, le cacao sent le lait froid.",
            "enfant-f|Tu as ouvert, tout haut.",
            "copain|Tu tenais les tasses.",
            "maman|Le verre sent le matin.",
            "papa|Le cacao est à vous, maintenant.",
            "narrateur|Le capuchon penche, un peu voilé de froid.",
            "narrateur|Nina verse dans la tasse petite.",
            "narrateur|Un rai traverse la vapeur, tout chaud.",
            "narrateur|Le loquet redevient silencieux, tout seul.",
        ),
        (1, 2, 2): L(
            "narrateur|Près du bac, deux paires de pieds se touchent.",
            "copain|Tu l'as trouvé, d'en bas.",
            "enfant-f|Tes yeux gardaient la porte.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du bac sèche.",
            "narrateur|Le capuchon penche, face à l'ombre du bac.",
            "copain|Il fume trop, Nina.",
            "enfant-f|C'est pour ça.",
            "narrateur|La porte garde le froid, tout proche.",
        ),
        (1, 2, 3): L(
            "narrateur|Un peu de vapeur reste au frigo.",
            "enfant-f|On a ouvert ensemble.",
            "copain|Sans trop monter.",
            "papa|Le tabouret est resté à sa place.",
            "maman|Vos mains sentent le lait.",
            "narrateur|Nina pose le bidon au rebord.",
            "narrateur|Le capuchon penche, et un clic répond.",
            "copain|Tu l'as eu.",
            "narrateur|La vapeur tremble un peu, puis s'endort.",
        ),
        (1, 3, 1): L(
            "narrateur|Sous la table, la grotte sent le bois.",
            "copain|Tu es passée, moi je fouettais.",
            "enfant-f|Tes épaules l'ont laissé ouvert.",
            "papa|Vous l'avez.",
            "maman|La petite tasse dort sur le bord.",
            "narrateur|Le capuchon penche, comme une lanterne éteinte.",
            "enfant-f|On reste un peu, Victorino.",
            "narrateur|Un rai brun s'endort sous le bois.",
            "narrateur|La miette redevient douce, autour.",
        ),
        (1, 3, 2): L(
            "narrateur|Le bord de table redescend, lentement.",
            "copain|Je suis rentré de côté.",
            "enfant-f|On a écarté, tous les deux.",
            "maman|Il n'était plus trop coincé.",
            "papa|La poudre danse, dans l'air.",
            "narrateur|Le capuchon penche, une éraflure de bois au métal.",
            "enfant-f|On souffle dessus.",
            "narrateur|Un rayon veille près des chaises.",
            "narrateur|Le radiateur se tait, contre le mur.",
        ),
        (1, 3, 3): L(
            "narrateur|Deux tasses se parlent, à travers le bois.",
            "copain|On a trinqué à travers.",
            "papa|La table vous a laissé la place.",
            "maman|Le secret tient, tout chaud.",
            "narrateur|Le capuchon penche, entre le dessous et le dessus.",
            "enfant-f|Regarde-le, Victorino, il fume.",
            "copain|Je le vois, d'ici.",
            "narrateur|Le brun reste au chaud, sous le bois.",
            "narrateur|Une chaise redevient simple, toute seule.",
        ),
        (2, 1, 1): L(
            "narrateur|À l'étagère, le fouet garde un fil brun.",
            "copain|Tu versais, moi je tournais.",
            "enfant-f|Tes bras ont vu le fond.",
            "papa|Vous l'avez, à deux.",
            "maman|Le bol dort sur le bois.",
            "narrateur|Le capuchon penche, et le fouet s'appuie contre.",
            "enfant-f|On reste un peu.",
            "narrateur|Un clic minuscule s'endort sur le plan.",
            "narrateur|La casserole se tait, sur le feu.",
        ),
        (2, 1, 2): L(
            "narrateur|Sur le tabouret, le fouet repose sur le genou.",
            "enfant-f|J'ai vu les fils, moi aussi.",
            "copain|Oui, tu étais assez haute.",
            "papa|Toi en bas, lui au-dessus, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            "narrateur|Le capuchon penche, une goutte au fil du fouet.",
            "copain|Je reste un peu.",
            "narrateur|Une goutte reste collée au bol.",
            "narrateur|L'évier sent le cacao, mêlé au métal.",
        ),
        (2, 1, 3): L(
            "narrateur|Le torchon redescend, le fouet au milieu.",
            "copain|Le bol est venu vers nous.",
            "enfant-f|On a tiré, tous les deux.",
            "maman|Il n'était plus trop haut.",
            "papa|La poudre danse, dans l'air.",
            "narrateur|Le capuchon penche, un fil de fouet au linge.",
            "enfant-f|On souffle dessus.",
            "narrateur|Un rayon veille près des bols.",
            "narrateur|Le radiateur se tait, au fond.",
        ),
        (2, 2, 1): L(
            "narrateur|Au frigo, le fouet garde un brin de froid.",
            "enfant-f|Tu as ouvert, tout haut.",
            "copain|Le clic a dit la poignée.",
            "maman|Le verre sent le matin.",
            "papa|Le cacao est à vous, maintenant.",
            "narrateur|Le capuchon penche, voilé, près du fouet.",
            "narrateur|Nina verse dans la tasse petite.",
            "narrateur|Un rai traverse la vapeur, tout chaud.",
            "narrateur|Le loquet redevient silencieux, tout seul.",
        ),
        (2, 2, 2): L(
            "narrateur|Près du bac, le fouet fait un dernier clic.",
            "copain|Tu l'as trouvé, d'en bas.",
            "enfant-f|Tes yeux gardaient la porte.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du bac sèche.",
            "narrateur|Le capuchon penche, et le fouet le salue.",
            "copain|Il fume trop, Nina.",
            "enfant-f|C'est pour ça.",
            "narrateur|La porte garde le froid, tout proche.",
        ),
        (2, 2, 3): L(
            "narrateur|Un peu de vapeur reste au frigo.",
            "enfant-f|On a ouvert ensemble.",
            "copain|Sans trop monter.",
            "papa|Le tabouret est resté à sa place.",
            "maman|Vos mains sentent le lait.",
            "narrateur|Nina pose le fouet au rebord.",
            "narrateur|Le capuchon penche, et le clic répond.",
            "copain|Tu l'as eu.",
            "narrateur|La vapeur tremble un peu, puis s'endort.",
        ),
        (2, 3, 1): L(
            "narrateur|Sous la table, le fouet fait un clic, tout bas.",
            "copain|Tu es passée, moi je fouettais.",
            "enfant-f|Tes épaules l'ont laissé ouvert.",
            "papa|Vous l'avez.",
            "maman|La petite tasse dort sur le bord.",
            "narrateur|Le capuchon penche, et le clic se tait.",
            "enfant-f|On reste un peu, Victorino.",
            "narrateur|Un rai brun s'endort sous le bois.",
            "narrateur|La miette redevient douce, autour.",
        ),
        (2, 3, 2): L(
            "narrateur|Le bord de table redescend, lentement.",
            "copain|Je suis rentré de côté.",
            "enfant-f|On a écarté, tous les deux.",
            "maman|Il n'était plus trop coincé.",
            "papa|La poudre danse, dans l'air.",
            "narrateur|Le capuchon penche, le fouet contre le pied.",
            "enfant-f|On souffle dessus.",
            "narrateur|Un rayon veille près des chaises.",
            "narrateur|Le radiateur se tait, contre le mur.",
        ),
        (2, 3, 3): L(
            "narrateur|Deux tasses se parlent, à travers le bois.",
            "copain|On a trinqué à travers.",
            "papa|La table vous a laissé la place.",
            "maman|Le secret tient, tout chaud.",
            "narrateur|Le capuchon penche, le fouet en nid.",
            "enfant-f|Regarde-le, Victorino, il fume.",
            "copain|J'entends le clic, d'ici.",
            "narrateur|Le brun reste au chaud, sous le bois.",
            "narrateur|Une chaise redevient simple, toute seule.",
        ),
        (3, 1, 1): L(
            "narrateur|À l'étagère, le plateau veille, deux tasses.",
            "copain|Tu versais, moi je tournais.",
            "enfant-f|Tes bras ont vu le fond.",
            "papa|Vous l'avez, à deux.",
            "maman|Le bol dort sur le bois.",
            "narrateur|Le capuchon penche, au-dessus de la petite tasse.",
            "enfant-f|On reste un peu.",
            "narrateur|Un rai brun s'endort sur les carreaux.",
            "narrateur|La casserole se tait, sur le feu.",
        ),
        (3, 1, 2): L(
            "narrateur|Sur le tabouret, deux tasses se calment.",
            "enfant-f|J'ai vu le fond, moi aussi.",
            "copain|Oui, tu étais assez haute.",
            "papa|Toi en bas, lui au-dessus, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            "narrateur|Le capuchon penche, une goutte dans la petite tasse.",
            "copain|Je reste un peu.",
            "narrateur|Une goutte reste collée au bol.",
            "narrateur|L'évier sent le cacao, et la porcelaine.",
        ),
        (3, 1, 3): L(
            "narrateur|Le torchon redescend, le plateau au creux.",
            "copain|Le bol est venu vers nous.",
            "enfant-f|On a tiré, tous les deux.",
            "maman|Il n'était plus trop haut.",
            "papa|La poudre danse, dans l'air.",
            "narrateur|Le capuchon penche, la petite tasse à l'ombre.",
            "enfant-f|On souffle dessus.",
            "narrateur|Un rayon veille près des bols.",
            "narrateur|Le radiateur se tait, au fond.",
        ),
        (3, 2, 1): L(
            "narrateur|Au frigo, le plateau garde un brin de froid.",
            "enfant-f|Tu as ouvert, tout haut.",
            "copain|Tu tenais les tasses.",
            "maman|Le verre sent le matin.",
            "papa|Le cacao est à vous, maintenant.",
            "narrateur|Le capuchon penche, entre les deux porcelaines.",
            "narrateur|Nina verse dans la tasse petite.",
            "narrateur|Un rai traverse la vapeur, tout chaud.",
            "narrateur|Le loquet redevient silencieux, tout seul.",
        ),
        (3, 2, 2): L(
            "narrateur|Près du bac, le plateau pose une ombre ronde.",
            "copain|Tu l'as trouvé, d'en bas.",
            "enfant-f|Tes yeux gardaient la porte.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du bac sèche.",
            "narrateur|Le capuchon penche, face aux deux tasses.",
            "copain|Il fume trop, Nina.",
            "enfant-f|C'est pour ça.",
            "narrateur|La porte garde le froid, tout proche.",
        ),
        (3, 2, 3): L(
            "narrateur|Un peu de vapeur reste au frigo.",
            "enfant-f|On a ouvert ensemble.",
            "copain|Sans trop monter.",
            "papa|Le tabouret est resté à sa place.",
            "maman|Vos mains sentent le lait.",
            "narrateur|Nina pose le plateau au rebord.",
            "narrateur|Le capuchon penche, et les tasses répondent.",
            "copain|Tu l'as eu.",
            "narrateur|La vapeur tremble un peu, puis s'endort.",
        ),
        (3, 3, 1): L(
            "narrateur|Sous la table, le plateau tient leurs coudes.",
            "copain|Tu es passée, moi je fouettais.",
            "enfant-f|Tes épaules l'ont laissé ouvert.",
            "papa|Vous l'avez.",
            "maman|La petite tasse dort sur le bord.",
            "narrateur|Le capuchon penche, au creux de la petite tasse.",
            "enfant-f|On reste un peu, Victorino.",
            "narrateur|Un rai brun s'endort sous le bois.",
            "narrateur|La miette redevient douce, autour.",
        ),
        (3, 3, 2): L(
            "narrateur|Le bord de table redescend, lentement.",
            "copain|Je suis rentré de côté.",
            "enfant-f|On a écarté, tous les deux.",
            "maman|Il n'était plus trop coincé.",
            "papa|La poudre danse, dans l'air.",
            "narrateur|Le capuchon penche, la grande tasse dehors.",
            "enfant-f|On souffle dessus.",
            "narrateur|Un rayon veille près des chaises.",
            "narrateur|Le radiateur se tait, contre le mur.",
        ),
        (3, 3, 3): L(
            "narrateur|Deux tasses se parlent, à travers le bois.",
            "copain|On a trinqué à travers.",
            "papa|La table vous a laissé la place.",
            "maman|Le secret tient, tout chaud.",
            "narrateur|Le capuchon penche, entre petite et grande.",
            "enfant-f|Regarde-le, Victorino, il fume.",
            "copain|Je vois la grande, d'ici.",
            "narrateur|Le brun reste au chaud, sous le bois.",
            "narrateur|Une chaise redevient simple, toute seule.",
        ),
    }
    return table[(t1, t2, t3)]


def write_tree() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    profiles: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|D'habitude, le bidon de cacao cliquette, dans le placard.",
        "narrateur|Là, le placard reste muet.",
        "narrateur|La casserole, elle, fait tic, sur le feu.",
        "narrateur|Les manteaux mouillés sentent la laine, près de la porte.",
        "narrateur|Nina connaît cette cuisine, presque par cœur.",
        "narrateur|Un détail, là-haut, paraît neuf.",
        "narrateur|Le bidon de cacao penche son capuchon, trop haut.",
        "enfant-f|Il n'était pas comme ça.",
        "maman|Le capuchon penche, c'est vrai.",
        "papa|Tu as vu le lait, Nina ?",
        "enfant-f|Il fume, dans la casserole.",
        "narrateur|En ce moment, Nina veut deux tasses, avant la peau du lait.",
        "enfant-f|Victorino, on fait du cacao, pour deux ?",
        "narrateur|Victorino arrive, plus grand, sans se presser.",
        "copain|J'arrive.",
        "papa|Le lait va se couvrir, si on attend.",
        "papa|Merci, tu as baissé le feu.",
    )
    sons["CHK_T0000_P0000"] = "casserole,pluie"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "capuchon"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Le bidon, le fouet, et les deux tasses attendent.",
        "maman|Tu prends quoi d'abord, Nina ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("le bidon de cacao", "le fouet", "les deux tasses")

    t2_sons = {1: "poudre,bol", 2: "frigo,porte", 3: "bois,chaise"}
    t2_emph = {1: "étagère", 2: "lait", 3: "table"}
    t3_emph = {
        1: {1: "bras", 2: "tabouret", 3: "torchon"},
        2: {1: "poignée", 2: "bac", 3: "tabouret"},
        3: {1: "passage", 2: "chaise", 3: "tasses"},
    }

    for t1 in (1, 2, 3):
        meta = T1[t1]
        base = f"CHK_T0001_P000{t1}"
        scripts[base] = t1_passage(t1)
        sons[base] = meta["sons"]
        profiles[base] = "action"
        emph[base] = meta["emph"]

        qid = f"{base}_Q0001"
        scripts[qid] = t1_q(t1)
        profiles[qid] = "clue"
        extras[qid] = qf(meta["ans"], meta["acc"], meta["retry"])
        emph[qid] = meta["emph"]

        cid = f"{base}_C0001"
        scripts[cid] = t1_confirm(t1)
        profiles[cid] = "confirm"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("l'étagère", "le frigo", "sous la table")

        for t2 in (1, 2, 3):
            p2 = f"{base}_T0002_P000{t2}"
            scripts[p2] = t2_scene(t1, t2)
            sons[p2] = t2_sons[t2]
            profiles[p2] = "obstacle"
            emph[p2] = t2_emph[t2]

            t3q = f"{p2}_T0003_P0000"
            scripts[t3q] = t3_question(t2)
            profiles[t3q] = "choice"
            extras[t3q] = t3lab(*T3_LABS[t2])

            for t3i in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{t3i}"
                scripts[p3] = t3_scene(t1, t2, t3i)
                sons[p3] = t2_sons[t2]
                profiles[p3] = "resolution"
                emph[p3] = t3_emph[t2][t3i]

                fin = f"{p3}_F0001"
                scripts[fin] = fin_scene(t1, t2, t3i)
                sons[fin] = "vapeur,tasses"
                profiles[fin] = "ending"
                emph[fin] = "capuchon"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        text, script = from_script(scripts[cid])
        nc = dict(c)
        nc["text"] = text
        nc["script"] = script
        nc["sons"] = sons.get(cid, c.get("sons") or "") or ""
        extra_voice: dict = {}
        if cid in emph:
            extra_voice["emphasis"] = emph[cid]
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            extra_voice["pause_before"] = 200
        nc.update(voice(text, profiles[cid], extra_voice or None))
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    fins = [c for c in out["chunks"] if c.get("kind") == "passage_fin"]
    texts = [c["text"] for c in fins]
    if len(texts) != 27:
        raise SystemExit(f"fins {len(texts)} != 27")
    if len(set(texts)) != 27:
        raise SystemExit("fins non distinctes")
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
        if "capuchon" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']} indice capuchon absent de la fin")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for tic in TICS + (
        "kenzo",
        "merle",
        "miel",
        "capitaine",
        "plic",
        "volet jaune",
        "pommier",
        "marelle",
        "soleil en papier",
        "bac à sable",
        "toboggan",
        "balançoire",
        "sami",
        "doudou",
        "bidon de lait",
        "grand-père",
        "maîtresse",
        "jardinier",
        "on va apprendre",
        "j'ai compris",
        "mission accomplie",
    ):
        if tic in whole:
            raise SystemExit(f"{SID} slogan/calque: {tic}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob or "victorino" not in blob:
        raise SystemExit(f"{SID}: troupe Nina/Victorino absente")
    if "capuchon" not in blob:
        raise SystemExit(f"{SID}: indice capuchon absent")
    for bad in ("déjà", "deja", "encore", "tout doux", "tout calme"):
        if bad in blob:
            raise SystemExit(f"{SID} tic corpus: {bad}")
    if not all(c.get("text_xai_tags") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags manquant")
    if not all(c.get("notes") for c in out["chunks"]):
        raise SystemExit(f"{SID}: notes manquant")
    if not all(c.get("text_ssml") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_ssml manquant")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    write_tree()
    relecture(
        SID,
        TITLE,
        "Cuisine après la pluie. La casserole fait tic. Nina veut deux tasses de cacao, "
        "avant la peau du lait. Indice unique : le capuchon qui penche, trop haut, "
        "payé à chaque climax et chaque fin. Victorino plus grand, rythme lent ; "
        "Nina propose. T1 = bidon / fouet / deux tasses (les trois partent). "
        "T2 = étagère (hauteur, deux envies) / frigo (lait manquant) / sous la table "
        "(grotte vs plan). Première idée rate (saut, porte qui claque, épaules coincées). "
        "T3 = neuf façons ; Nina refuse de foncer, revoit le capuchon. "
        "Leçon DIF.COR.001 vécue (deux hauteurs), jamais dite. 27 fins distinctes.",
        "F-NAR-019 example4 v2. N3 ≤ 16. Tics encore/déjà/tout doux/tout calme jetés. "
        "Sami/Léa/Tom, merle, miel, Mission accomplie, J'ai compris jetés. "
        "Monde ≠ TREE-AUT-019 (cacao, étagère, deux tasses). "
        "TTS notes+ssml+xai+piper par chunk (profiles example2). "
        "Un merci de papa (baisser le feu). Pas apply. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
