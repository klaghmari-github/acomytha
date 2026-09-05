#!/usr/bin/env python3
"""TREE-COL-031 — F-NAR-019 : moufles, bateau en papier, 27 fins, TTS."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-COL-031"
N3 = LIMITS["N3"]
CHILD = "enfant-m"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="bateau en papier",
        note="arc=installation; intention=émerveiller; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=un voyage trop pressé; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=on_t_a_entendu; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_partir_tout_de_suite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=la_voile_peut_boire; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=écouter_change_le_voyage; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=les_moufles_et_le_bateau_ont_leur_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    if m.get("emphasis"):
        e = esc(m["emphasis"])
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    if m.get("emphasis"):
        em = m["emphasis"]
        body = body.replace(em, f"<emphasis>{em}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        tag = m["pitch_tag"]
        body = f"<{tag}>{body}</{tag}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def split_sents(phrase: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    for ch in phrase:
        buf.append(ch)
        if ch in ".?!":
            s = "".join(buf).strip()
            if s:
                parts.append(s)
            buf = []
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail if tail.endswith((".", "?", "!")) else tail + ".")
    return parts


def ln(role: str, phrase: str) -> str:
    n = words(phrase)
    if n > N3:
        raise SystemExit(f"{n}>{N3}: {phrase}")
    if n == 0:
        raise SystemExit(f"vide: {role}|{phrase}")
    marks = phrase.count(".") + phrase.count("?") + phrase.count("!")
    if marks != 1:
        raise SystemExit(f"ponctuation {marks}: {phrase}")
    if not phrase.endswith((".", "?", "!")):
        raise SystemExit(f"fin: {phrase}")
    return f"{role}|{phrase}"


def L(*pairs: tuple[str, str]) -> list[str]:
    out: list[str] = []
    for role, phrase in pairs:
        for sent in split_sents(phrase):
            out.append(ln(role, sent))
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> dict:
    m = dict(PROFILES[profile])
    if extra:
        if "emphasis" in extra:
            m["emphasis"] = extra["emphasis"]
        if "note" in extra:
            m["note"] = extra["note"]
    text, script = from_script(lines)
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
    out["pitch_ssml"] = m["pitch_ssml"]
    out["pitch_xai_tag"] = m["pitch_tag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m["emphasis"] or ""
    out["pause_before_ms"] = (extra or {}).get("pause_before", 0)
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
    out["night_policy"] = (extra or {}).get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    fields = (extra or {}).get("fields") or {}
    out.update(fields)
    return out


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put(
        "CHK_T0000_P0000",
        L(
            ("narrateur", "Dans le village, la petite maison a les volets fermés sous la pluie."),
            ("narrateur", "Victorino y vit avec papa et maman."),
            ("narrateur", "Le radiateur du salon fait tic, un petit métal chaud."),
            ("narrateur", "Les moufles bleues de Victorino sèchent dessus."),
            ("narrateur", "Elles sentent la laine mouillée."),
            ("narrateur", "Sur le rebord, un bateau en papier attend, voile un peu pliée."),
            ("narrateur", "Dehors, la gouttière chante une note longue."),
            ("narrateur", "Dans la cuisine, maman essore un manteau lourd."),
            ("narrateur", "Papa aligne les bottes près du paillasson."),
            ("narrateur", "Une petite flaque brille sous une semelle."),
            ("narrateur", "En ce moment, Victorino tient son bateau à deux mains."),
            ("enfant-m", "Papa, maman, il est prêt !"),
            ("narrateur", "Papa parle du manteau, et maman lui répond."),
            ("narrateur", "Les mots de Victorino se perdent entre les gouttes."),
            ("narrateur", "Une goutte tombe d'une moufle, pile sur la voile."),
            ("narrateur", "Le papier devient plus sombre."),
            ("enfant-m", "Si personne n'écoute, il va trop boire !"),
            ("maman", "Tu disais quelque chose, Victorino ?"),
            ("enfant-m", "Le bateau va trop boire."),
            ("papa", "On vient. Montre-nous où il peut partir."),
            ("narrateur", "Victorino referme la bouche, puis cherche un endroit."),
        ),
        "opening",
        "pluie,radiateur",
    )

    put(
        "CHK_T0001_P0000",
        L(
            ("narrateur", "Pour le premier voyage, trois endroits peuvent recevoir l'eau."),
            ("maman", "Le tapis, la table, ou la fenêtre ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "le tapis", "option_2_label": "la table", "option_3_label": "la fenêtre"}},
    )

    # --- T1 lieux ---
    put(
        "CHK_T0001_P0001",
        L(
            ("narrateur", "Victorino pose une serviette épaisse sur le tapis gris."),
            ("narrateur", "Le tapis gratte un peu sous ses genoux."),
            ("narrateur", "Il pose un bassin en zinc, froid au doigt."),
            ("papa", "Je verse l'eau des bottes, sans me presser."),
            ("narrateur", "L'eau claque quand même, et une vague lèche la serviette."),
            ("enfant-m", "Regardez, il part !"),
            ("narrateur", "Maman parle du manteau qui goutte, près du radiateur."),
            ("narrateur", "Victorino a parlé dans ses mots."),
            ("narrateur", "Personne ne se baisse vers le bassin."),
            ("narrateur", "Le bateau penche. La voile boit trop."),
            ("narrateur", "Victorino se tait. Il touche le coude de papa."),
            ("enfant-m", "Quand tu as fini, je peux montrer le départ ?"),
            ("papa", "Oui. La botte est posée. Je t'écoute."),
            ("narrateur", "Cette fois, papa et maman s'accroupissent près du zinc."),
            ("maman", "La voile tremble. Que lui faut-il, d'après toi ?"),
        ),
        "action",
        "bassin,serviette",
        {"emphasis": "bassin en zinc"},
    )
    put(
        "CHK_T0001_P0001_Q0001",
        L(
            ("narrateur", "Victorino a parlé trop vite, sur le tapis."),
            ("maman", "Que fait-il avant de recommencer ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "attendre",
                "accepted_examples": "attendre | il attend | se taire | écouter",
                "retry_prompt": "Il se tait un moment. Ensuite ?",
                "engine_ok_text": "Oui, il attend que papa finisse.",
                "engine_near_text": "Tu es tout près. Écoute encore l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0001_C0001",
        L(
            ("maman", "Oui. Il attend la fin de la phrase."),
            ("narrateur", "Papa pose enfin la deuxième botte."),
            ("papa", "Voilà. Ton bassin a toute mon oreille."),
            ("enfant-m", "Le bateau penche. Il a trop d'eau."),
            ("maman", "Merci d'avoir attendu ma phrase, Victorino."),
            ("narrateur", "Tous les trois regardent le zinc, sans se couper."),
            ("narrateur", "La voile tremble, mais elle tient."),
        ),
        "confirm",
        "bassin",
        {"emphasis": "zinc"},
    )
    put(
        "CHK_T0001_P0001_T0002_P0000",
        L(
            ("narrateur", "Sur le tapis, le bateau penche un peu."),
            ("papa", "On ouvre le livre, on tape la pluie, ou on trace un trait ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "l'histoire", "option_2_label": "la chanson", "option_3_label": "le dessin"}},
    )

    put(
        "CHK_T0001_P0002",
        L(
            ("narrateur", "Victorino pousse un plat creux au milieu de la table."),
            ("narrateur", "Le bois sent l'orange que maman vient d'éplucher."),
            ("narrateur", "Papa verse l'eau de pluie, prise dans la casserole."),
            ("narrateur", "Une pelure glisse, comme une île jaune."),
            ("enfant-m", "Mon bateau va tourner autour !"),
            ("narrateur", "Maman répond à papa au sujet du manteau."),
            ("narrateur", "Leurs voix se mélangent, et le cri se perd."),
            ("narrateur", "Le bateau heurte la pelure. La voile se plisse."),
            ("narrateur", "Victorino serre les lèvres. Il pose le bateau."),
            ("enfant-m", "Je peux parler quand l'orange est dans l'assiette ?"),
            ("maman", "Oui. L'assiette est prête. Nous t'écoutons."),
            ("papa", "Quelle île veux-tu pour ton voyage ?"),
            ("narrateur", "Le plat attend, rond et clair, au centre du bois."),
        ),
        "action",
        "table,eau",
        {"emphasis": "plat creux"},
    )
    put(
        "CHK_T0001_P0002_Q0001",
        L(
            ("narrateur", "À la table, personne n'a entendu le premier cri."),
            ("papa", "Que fait Victorino maintenant ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "attendre",
                "accepted_examples": "attendre | il attend | se taire | écouter",
                "retry_prompt": "Il pose le bateau. Ensuite ?",
                "engine_ok_text": "Oui, il attend que maman finisse.",
                "engine_near_text": "Tu es tout près. Écoute encore l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0002_C0001",
        L(
            ("papa", "Oui. Il a attendu l'assiette."),
            ("narrateur", "Maman pose la pelure sur le bord, hors du plat."),
            ("maman", "Maintenant, le voyage a de la place."),
            ("enfant-m", "La voile s'est plissée. On peut l'aider."),
            ("papa", "Merci d'avoir laissé finir l'orange."),
            ("narrateur", "Le bois de la table brille, un peu collant."),
            ("narrateur", "Le bateau attend au bord, plus droit."),
        ),
        "confirm",
        "table",
        {"emphasis": "orange"},
    )
    put(
        "CHK_T0001_P0002_T0002_P0000",
        L(
            ("narrateur", "À la table, la voile reste un peu froissée."),
            ("maman", "Le livre, le rythme, ou le crayon ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "l'histoire", "option_2_label": "la chanson", "option_3_label": "le dessin"}},
    )

    put(
        "CHK_T0001_P0003",
        L(
            ("narrateur", "Victorino ouvre un peu la fenêtre. L'air sent le toit mouillé."),
            ("narrateur", "Un bol en bois attend sur le rebord, sous la gouttière."),
            ("narrateur", "Chaque goutte y fait un rond, puis un autre."),
            ("enfant-m", "Il peut partir avec la pluie !"),
            ("narrateur", "Le vent pousse la vitre, et papa parle du loquet."),
            ("narrateur", "La phrase de Victorino part avec le courant d'air."),
            ("narrateur", "Le bateau glisse vers le bord. Presque trop loin."),
            ("narrateur", "Victorino rattrape la coque, sans crier."),
            ("enfant-m", "Quand le loquet est fermé, je montre le bol ?"),
            ("papa", "Oui. Le loquet claque. Nous t'écoutons."),
            ("maman", "Le vent est fort. Que crains-tu, pour la voile ?"),
            ("narrateur", "Le bol tremble. L'eau y danse, toute ronde."),
        ),
        "action",
        "gouttiere,vitre",
        {"emphasis": "bol en bois"},
    )
    put(
        "CHK_T0001_P0003_Q0001",
        L(
            ("narrateur", "À la fenêtre, le vent a couvert sa voix."),
            ("maman", "Que fait Victorino avant de reparler ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "attendre",
                "accepted_examples": "attendre | il attend | se taire | écouter",
                "retry_prompt": "Il rattrape le bateau. Ensuite ?",
                "engine_ok_text": "Oui, il attend que le loquet soit fermé.",
                "engine_near_text": "Tu es tout près. Écoute encore l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0003_C0001",
        L(
            ("maman", "Oui. Il a attendu le loquet."),
            ("narrateur", "Papa ferme. Le vent reste dehors."),
            ("papa", "Le bol est à toi. Nous regardons."),
            ("enfant-m", "Il a failli tomber. La voile a peur."),
            ("maman", "Merci d'avoir parlé après le clac."),
            ("narrateur", "Une goutte de gouttière tombe juste au centre."),
            ("narrateur", "Le bateau tient, collé au bois du bol."),
        ),
        "confirm",
        "loquet",
        {"emphasis": "loquet"},
    )
    put(
        "CHK_T0001_P0003_T0002_P0000",
        L(
            ("narrateur", "À la fenêtre, le vent a bougé la voile."),
            ("papa", "Une image, une chanson, ou un trait ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "l'histoire", "option_2_label": "la chanson", "option_3_label": "le dessin"}},
    )

    # --- T2 selon lieu ---
    t2 = {
        ("tapis", "histoire"): (
            L(
                ("narrateur", "Maman pose un livre d'images au bord de la serviette."),
                ("narrateur", "Une page montre un bateau blanc, voile bien droite."),
                ("maman", "Regarde : sa voile ne touche pas l'eau."),
                ("enfant-m", "La mienne, elle touche, elle est trop lourde !"),
                ("narrateur", "Victorino a parlé pendant la phrase de maman."),
                ("narrateur", "Une éclaboussure atteint le coin de la page."),
                ("narrateur", "Le papier du livre se gondole, tout petit."),
                ("papa", "Attends qu'elle finisse la page, puis tu montres."),
                ("narrateur", "Victorino serre le bateau. Il écoute la fin."),
                ("maman", "Voilà. Ta voile a besoin d'un peu d'air, comme celle-là."),
                ("enfant-m", "On peut la redresser sans la mouiller plus ?"),
                ("narrateur", "Le livre reste ouvert, loin du zinc, cette fois."),
            ),
            "pages,bassin",
            "voile",
        ),
        ("tapis", "chanson"): (
            L(
                ("narrateur", "Papa tape le bord du bassin, comme la gouttière."),
                ("narrateur", "Toc, toc, toc, toc : quatre petits coups."),
                ("papa", "Au quatrième, le bateau peut partir."),
                ("enfant-m", "Il part !"),
                ("narrateur", "Victorino lâche trop tôt, au deuxième toc."),
                ("narrateur", "L'eau saute. La serviette prend une tache ronde."),
                ("maman", "Le rythme n'était pas fini. Tu as entendu les quatre ?"),
                ("narrateur", "Victorino secoue la tête. Ses joues chauffent."),
                ("enfant-m", "Je recommence. J'écoute les tocs jusqu'au bout."),
                ("narrateur", "Papa reprend, plus lent. Personne ne parle par-dessus."),
                ("narrateur", "Les moufles, au radiateur, bougent un peu à chaque toc."),
            ),
            "tapotement,bassin",
            "toc",
        ),
        ("tapis", "dessin"): (
            L(
                ("narrateur", "Maman prend un crayon bleu, mine un peu grasse."),
                ("narrateur", "Elle veut tracer une ligne sur la coque, hors de l'eau."),
                ("enfant-m", "Je la fais !"),
                ("narrateur", "Victorino attrape le crayon pendant le premier trait."),
                ("narrateur", "La ligne part de travers, vers le zinc."),
                ("papa", "Le papier est fragile. Laisse-la finir le bord."),
                ("narrateur", "Victorino rend le crayon. Il souffle par le nez."),
                ("maman", "Merci. Maintenant, un trait droit, comme un quai."),
                ("narrateur", "Le bleu sèche au-dessus de l'eau, une lèvre mince."),
                ("enfant-m", "Si l'eau monte, on verra le danger."),
                ("narrateur", "Le crayon repose sur la serviette, loin des vagues."),
            ),
            "crayon,serviette",
            "trait bleu",
        ),
        ("table", "histoire"): (
            L(
                ("narrateur", "Maman ouvre le livre à côté du plat, loin de l'eau."),
                ("narrateur", "Sur l'image, un bateau tourne autour d'une île ronde."),
                ("maman", "Comme ta pelure, tout à l'heure."),
                ("enfant-m", "Mon île, c'est l'orange !"),
                ("narrateur", "Il le dit pendant qu'elle montre le dessin."),
                ("narrateur", "Papa recule le livre. Une goutte menaçait la page."),
                ("papa", "On écoute la page, puis on compare l'île."),
                ("narrateur", "Victorino met les mains à plat sur le bois."),
                ("maman", "L'image est finie. Ton île peut rester au bord."),
                ("enfant-m", "Le bateau la contourne, sans la manger."),
                ("narrateur", "L'odeur d'orange reste, plus forte que la pluie."),
            ),
            "pages,orange",
            "île",
        ),
        ("table", "chanson"): (
            L(
                ("narrateur", "Papa frappe le bois de la table, trois coups sourds."),
                ("narrateur", "La carafe vibre. L'eau du plat fait des ronds."),
                ("papa", "Trois coups, puis le départ, pas avant."),
                ("enfant-m", "Un, deux… maintenant !"),
                ("narrateur", "Il pousse trop tôt. Le plat glisse d'un doigt."),
                ("maman", "Le troisième coup n'était pas là. Tu l'as entendu ?"),
                ("narrateur", "Victorino écoute. Le troisième coup arrive, plus grave."),
                ("enfant-m", "Celui-là, je le garde dans la tête."),
                ("papa", "Bien. On recommence le rythme, sans se couper."),
                ("narrateur", "Les cuillères dans le tiroir répondent, tout loin."),
            ),
            "tapotement,table",
            "trois coups",
        ),
        ("table", "dessin"): (
            L(
                ("narrateur", "Maman essuie un peu d'orange sur ses doigts."),
                ("narrateur", "Elle trace, sur la coque, une ligne bleu pâle."),
                ("enfant-m", "Plus bas, plus bas !"),
                ("narrateur", "Victorino parle trop près. Le crayon dérape."),
                ("narrateur", "Un trait gras traverse presque le pli de la voile."),
                ("papa", "On laisse la ligne se poser, sans souffler dessus."),
                ("narrateur", "Victorino recule sa chaise d'un cran."),
                ("maman", "Le bleu dit : ici l'eau, ici le sec."),
                ("enfant-m", "Si ça dépasse, on arrête le voyage."),
                ("narrateur", "La mine repose près de la pelure, propre cette fois."),
            ),
            "crayon,table",
            "ligne bleu pâle",
        ),
        ("fenetre", "histoire"): (
            L(
                ("narrateur", "Maman tient le livre contre la vitre embuée."),
                ("narrateur", "Le bateau de la page regarde le bateau du bol."),
                ("maman", "Le sien a une voile haute, loin des vagues."),
                ("enfant-m", "Le mien est plus petit, mais il est vrai !"),
                ("narrateur", "Sa voix recouvre la fin de la phrase."),
                ("narrateur", "Une goutte de gouttière éclabousse le rebord."),
                ("papa", "Laisse-la comparer, puis tu présentes le tien."),
                ("narrateur", "Victorino attend. Maman baisse le livre."),
                ("maman", "Ton vrai bateau a besoin du même air, plus haut."),
                ("enfant-m", "On relève la voile, sans le sortir du bol."),
                ("narrateur", "Les deux bateaux se font face, papier contre papier."),
            ),
            "pages,vitre",
            "deux bateaux",
        ),
        ("fenetre", "chanson"): (
            L(
                ("narrateur", "La gouttière chante une note, puis une pause."),
                ("papa", "On part sur la note longue, pas sur la courte."),
                ("enfant-m", "C'est maintenant !"),
                ("narrateur", "Il pousse sur la note courte. Le bol bascule."),
                ("narrateur", "Papa rattrape le bois. Un peu d'eau file au rebord."),
                ("maman", "Tu as entendu la longue, celle qui dure ?"),
                ("narrateur", "Victorino colle l'oreille vers le tuyau."),
                ("enfant-m", "Elle vient. Elle est plus grave."),
                ("papa", "On attend celle-là. Personne ne parle par-dessus."),
                ("narrateur", "La note longue arrive, et le bol se tient."),
            ),
            "gouttiere,bol",
            "note longue",
        ),
        ("fenetre", "dessin"): (
            L(
                ("narrateur", "Maman trace un trait bleu sur la coque, près du bol."),
                ("narrateur", "Le vent fait bouger le papier sous la mine."),
                ("enfant-m", "Je tiens, moi !"),
                ("narrateur", "Il attrape trop fort. Le trait devient un virage."),
                ("papa", "On attend que le vent passe, puis un trait droit."),
                ("narrateur", "Victorino lâche. Une rafale s'en va."),
                ("maman", "Merci. Voici le quai, bien net, au-dessus de l'eau."),
                ("enfant-m", "Si l'eau monte au bleu, on rentre au port."),
                ("narrateur", "Un petit trait de doigt reste aussi sur la vitre."),
                ("narrateur", "Le crayon se repose sur le rebord, à l'abri."),
            ),
            "crayon,vitre",
            "trait de doigt",
        ),
    }

    lieu_key = {"1": "tapis", "2": "table", "3": "fenetre"}
    act_key = {"1": "histoire", "2": "chanson", "3": "dessin"}
    obj_key = {"1": "doudou", "2": "camion", "3": "gobelet"}
    lieu_id = {"tapis": "1", "table": "2", "fenetre": "3"}
    act_id = {"histoire": "1", "chanson": "2", "dessin": "3"}

    t3_q = {
        ("tapis", "histoire"): "Pour tenir le bateau comme sur la page, trois aides attendent.",
        ("tapis", "chanson"): "Pour partir au bon toc, trois aides attendent sur le tapis.",
        ("tapis", "dessin"): "Pour garder l'eau sous le trait, trois aides attendent.",
        ("table", "histoire"): "Pour contourner l'île d'orange, trois aides attendent.",
        ("table", "chanson"): "Pour partir au troisième coup, trois aides attendent.",
        ("table", "dessin"): "Pour respecter la ligne bleue, trois aides attendent.",
        ("fenetre", "histoire"): "Pour garder la voile haute, trois aides attendent au rebord.",
        ("fenetre", "chanson"): "Pour partir sur la note longue, trois aides attendent.",
        ("fenetre", "dessin"): "Pour garder le quai bleu, trois aides attendent à la fenêtre.",
    }

    for li in "123":
        for ac in "123":
            lieu = lieu_key[li]
            act = act_key[ac]
            lines, sons, emph = t2[(lieu, act)]
            cid = f"CHK_T0001_P000{li}_T0002_P000{ac}"
            put(cid, lines, "obstacle", sons, {"emphasis": emph})
            qcid = f"{cid}_T0003_P0000"
            put(
                qcid,
                L(
                    ("narrateur", t3_q[(lieu, act)]),
                    ("papa", "Le doudou, le camion, ou le gobelet ?"),
                ),
                "choice",
                "",
                {"fields": {"option_1_label": "le doudou", "option_2_label": "le camion", "option_3_label": "le gobelet"}},
            )

    # --- 27 T3 + 27 fins ---
    scenes = t3_scenes()
    for li in "123":
        for ac in "123":
            for ob in "123":
                lieu, act, obj = lieu_key[li], act_key[ac], obj_key[ob]
                passage, ending, s3, se, emph = scenes[(lieu, act, obj)]
                base = f"CHK_T0001_P000{li}_T0002_P000{ac}_T0003_P000{ob}"
                put(base, passage, "resolution", s3, {"emphasis": emph})
                put(f"{base}_F0001", ending, "ending", se, {"emphasis": "moufles"})

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = []
    for c in src["chunks"]:
        if c["kind"] == "passage_fin":
            ends.append(out_chunks[c["chunk_id"]]["text"])
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    t3_texts = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        if cid.endswith("T0003_P0001") or cid.endswith("T0003_P0002") or cid.endswith("T0003_P0003"):
            if "_F0001" not in cid and "P0000" not in cid.split("T0003_")[-1]:
                t3_texts.append(out_chunks[cid]["text"])
    # 27 passages T3
    t3_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Sous la pluie, les moufles bleues de Victorino sèchent sur le radiateur. "
        "Il veut faire partir son bateau en papier tout de suite, avant que la voile ne boive trop. "
        "Sa première phrase se perd dans les manteaux mouillés. "
        "Le bassin sur le tapis, le plat sur la table ou le bol à la fenêtre changent le danger. "
        "Un livre, un rythme ou un trait bleu préparent la voile. "
        "Le doudou, le camion ou le gobelet décident le vrai départ. "
        "Le soir, les moufles sont chaudes et le bateau a une place unique, parce que chacun a écouté jusqu'au bout."
    )
    merged["title"] = "Les moufles et le bateau en papier"
    merged["characters"] = "Victorino, papa, maman"
    merged["setting"] = "petite maison du village, salon et cuisine, matin de pluie"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    relecture(
        SID,
        "Les moufles et le bateau en papier",
        (
            "Victorino veut lancer son bateau en papier avant que la voile ne se gorge. "
            "Il crie trop tôt : papa et maman parlent des manteaux. Une goutte de moufle sombre la voile. "
            "Tapis (bassin), table (plat et île d'orange) ou fenêtre (bol et gouttière) changent l'obstacle. "
            "Livre, rythme ou trait bleu changent la préparation. "
            "Doudou, camion ou gobelet changent le climax. 27 fins : moufles sèches + place unique du bateau."
        ),
        (
            "Reprise complète F-NAR-019. Classe → maison sous la pluie. "
            "T3 Léa/Tom/Sami → doudou/camion/gobelet. "
            "Plus de refrain « on lève la main / puis on parle ». "
            "Première phrase perdue, puis attente vécue. "
            "27 fins textuellement distinctes. TTS (profils opening/choice/clue/confirm/action/obstacle/resolution/ending). "
            "N3 ≤ 16. check() OK. Pas d'apply."
        ),
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks")


def t3_scenes() -> dict[tuple[str, str, str], tuple]:
    """27 climats : passage, ending, sons_t3, sons_fin, emphasis."""
    N = "narrateur"
    E = CHILD
    P = "papa"
    M = "maman"

    def S(*rows):
        return L(*rows)

    data = {}

    # TAPIS + HISTOIRE
    data[("tapis", "histoire", "doudou")] = (
        S(
            (N, "Victorino va chercher son doudou gris, une oreille plus chaude."),
            (N, "Il le pose trop vite au bord du zinc, comme un quai."),
            (E, "Toi, tu tiens le bateau, comme sur la page !"),
            (N, "Une vague mouille la patte. Le livre manque de sauter."),
            (M, "Attends que la vague retombe, puis tu places l'oreille."),
            (N, "Victorino attend. L'eau se calme, ronde et grise."),
            (N, "Il glisse l'oreille du doudou, hors de l'eau cette fois."),
            (N, "Le bateau s'appuie contre la patte, voile plus droite."),
            (P, "Le quai de fourrure tient. La page du livre, aussi."),
        ),
        S(
            (N, "Le soir, le radiateur tic plus lent, dans le salon."),
            (M, "Raconte-nous le voyage, jusqu'au bout."),
            (E, "Le doudou a fait le quai, et le bateau a copié la page."),
            (P, "Nous t'avons entendu sans te couper."),
            (N, "Les moufles bleues sont chaudes, sèches, un peu rêche."),
            (N, "Le bateau sèche contre la patte du doudou, sur la serviette."),
            (N, "Une oreille garde une petite tache d'eau, presque invisible."),
        ),
        "doudou,bassin",
        "radiateur,tissu",
        "doudou",
    )
    data[("tapis", "histoire", "camion")] = (
        S(
            (N, "Victorino ramène le petit camion rouge, une roue qui crisse."),
            (N, "Il veut s'en servir comme rampe, collée au livre ouvert."),
            (E, "Il monte, puis il glisse, comme l'image !"),
            (N, "Le camion roule trop tôt. Une goutte atteint le coin de page."),
            (P, "On attend que maman tienne le livre, puis tu roules."),
            (N, "Victorino pose les roues. Il compte dans sa tête."),
            (M, "Le livre est prêt. La rampe peut avancer."),
            (N, "Le bateau glisse du livre au zinc, sans boire."),
            (N, "Le camion s'arrête, benne ouverte, comme un port sec."),
        ),
        S(
            (N, "Plus tard, la pluie s'éloigne derrière les volets."),
            (P, "On t'écoute. Toute la rampe, s'il te plaît."),
            (E, "Le camion a fait la rampe, et le livre n'a plus de goutte."),
            (M, "Merci d'avoir attendu ma page."),
            (N, "Les moufles pendent, chaudes, au-dessus du tic du radiateur."),
            (N, "Le bateau dort dans la benne, sur la serviette grise."),
            (N, "Une roue a laissé un fil d'eau, presque parti."),
        ),
        "camion,pages",
        "radiateur,roue",
        "rampe",
    )
    data[("tapis", "histoire", "gobelet")] = (
        S(
            (N, "Victorino prend le gobelet jaune, un peu froid."),
            (N, "Sur la page, une rivière mince rejoint le bateau blanc."),
            (E, "Je fais la rivière !"),
            (N, "Il verse trop vite. Le livre recule. La serviette s'assombrit."),
            (M, "La rivière de l'image est fine. On verse après ma phrase."),
            (N, "Victorino attend. Maman pose le livre plus haut."),
            (N, "Il penche le gobelet, un filet, pas une cascade."),
            (N, "Le bateau suit le filet et s'ancre dans le gobelet."),
            (P, "Ton port jaune tient. La page, elle, est sèche."),
        ),
        S(
            (N, "Le salon sent la laine chaude, et un peu de zinc."),
            (M, "Dis-nous la rivière, sans rien sauter."),
            (E, "Le gobelet est devenu le port, comme la rivière du livre."),
            (P, "Nous t'avons suivi jusqu'au filet."),
            (N, "Les moufles sèches gardent la forme des mains."),
            (N, "Le bateau flotte dans le jaune, une coque minuscule."),
            (N, "Le livre est fermé, coin net, loin de l'eau."),
        ),
        "gobelet,eau",
        "radiateur,livre",
        "filet",
    )

    # TAPIS + CHANSON
    data[("tapis", "chanson", "doudou")] = (
        S(
            (N, "Victorino assied le doudou au bord, une oreille vers le zinc."),
            (E, "Toi, tu écoutes les tocs. Tu es le capitaine."),
            (N, "Au deuxième toc, il pousse le bateau vers la patte."),
            (N, "L'eau gicle. L'oreille du doudou prend une goutte."),
            (P, "Le capitaine attend le quatrième. Tu l'as entendu, toi ?"),
            (N, "Victorino hoche. Il reprend le bateau, joues chaudes."),
            (N, "Quatre tocs. Au dernier, le bateau rejoint la patte."),
            (M, "L'oreille est un peu mouillée, mais le rythme est entier."),
            (N, "Le doudou reste droit, capitaine silencieux."),
        ),
        S(
            (N, "Le radiateur tic comme un cinquième toc, plus doux."),
            (P, "Chante-nous les quatre coups, jusqu'au dernier."),
            (E, "Le doudou a attendu le quatrième, et le bateau aussi."),
            (M, "Ton capitaine a des oreilles patientes."),
            (N, "Les moufles bougent à peine, sèches, au-dessus du métal."),
            (N, "Le bateau sèche contre l'oreille, une voile un peu rêche."),
            (N, "Une tache d'eau s'efface sur le gris du doudou."),
        ),
        "doudou,tapotement",
        "radiateur,tissu",
        "capitaine",
    )
    data[("tapis", "chanson", "camion")] = (
        S(
            (N, "Victorino pose le camion rouge, cabine face au bassin."),
            (E, "Les roues font le tambour, avec papa."),
            (N, "Il pousse dès le premier toc. Une roue avale de l'eau."),
            (M, "Le tambour n'a pas fini. On roule au quatrième."),
            (N, "Victorino recule le camion. L'eau s'apaise."),
            (N, "Papa reprend les tocs. Les roues restent sages."),
            (N, "Au quatrième, le camion escorte le bateau, sans éclabousser."),
            (P, "Ta remorque a gardé le rythme. Merci d'avoir attendu."),
            (N, "Une petite trace de roue brille sur la serviette."),
        ),
        S(
            (N, "Dehors, la gouttière se tait, peu à peu."),
            (M, "On t'écoute : les tocs, puis les roues."),
            (E, "Le camion a escorté au quatrième toc, pas avant."),
            (P, "Le tambour et la remorque se sont parlé."),
            (N, "Les moufles sont tièdes, paires collées l'une à l'autre."),
            (N, "Le bateau voyage dans la benne, voile vers la cabine."),
            (N, "La trace de roue a séché, un croissant pâle."),
        ),
        "camion,tapotement",
        "radiateur,roue",
        "tambour",
    )
    data[("tapis", "chanson", "gobelet")] = (
        S(
            (N, "Victorino tapote le gobelet : il sonne, clair, comme une cloche."),
            (E, "La cloche dit le départ !"),
            (N, "Il verse pendant le son. L'eau saute hors du zinc."),
            (P, "On verse après le son, quand c'est retombé."),
            (N, "Victorino attend le silence du plastique jaune."),
            (N, "Papa fait les quatre tocs. Le gobelet se tait."),
            (N, "Alors seulement, un filet rejoint le bateau."),
            (M, "La cloche a parlé, puis l'eau. Chacun son temps."),
            (N, "Le bateau entre dans le gobelet, au dernier toc."),
        ),
        S(
            (N, "Le salon a deux musiques : le radiateur, et plus rien dehors."),
            (P, "Raconte la cloche, puis le filet."),
            (E, "J'ai versé après le son, et le bateau a un port jaune."),
            (M, "Merci d'avoir laissé finir la cloche."),
            (N, "Les moufles sèches sentent un peu la pluie, très loin."),
            (N, "Le gobelet garde le bateau, une cloche devenue quai."),
            (N, "La serviette a une tache ronde, plus claire maintenant."),
        ),
        "gobelet,tapotement",
        "radiateur,cloche",
        "cloche",
    )

    # TAPIS + DESSIN
    data[("tapis", "dessin", "doudou")] = (
        S(
            (N, "Victorino met le crayon dans la patte du doudou."),
            (E, "Toi, tu tiens le phare bleu."),
            (N, "Il veut lancer tout de suite. Le trait n'est pas sec."),
            (N, "Le bleu bave vers l'eau. Un nuage pâle se forme."),
            (M, "On attend que le phare sèche, puis le départ."),
            (N, "Victorino souffle à côté, pas dessus."),
            (N, "Le trait devient net. Le doudou reste le phare."),
            (N, "Le bateau part et s'arrête sous la patte, pile au bleu."),
            (P, "Ton phare a tenu. Le crayon, aussi."),
        ),
        S(
            (N, "La lumière du salon baisse. Le radiateur garde sa rondeur."),
            (M, "Dis-nous le phare, sans rien presser."),
            (E, "Le doudou tenait le crayon, et le bateau s'est arrêté au bleu."),
            (P, "Le trait a eu le temps de sécher."),
            (N, "Les moufles, sèches, ont un fil de laine relevé."),
            (N, "Le bateau sèche sous la patte, ligne bleue vers le zinc."),
            (N, "Le crayon repose, mine vers le haut, loin de l'eau."),
        ),
        "doudou,crayon",
        "radiateur,tissu",
        "phare",
    )
    data[("tapis", "dessin", "camion")] = (
        S(
            (N, "Maman dessine un quai sur un coin de serviette, tout petit."),
            (N, "Victorino veut y garer le camion tout de suite."),
            (N, "Les roues passent sur le crayon, trop gras."),
            (P, "Le quai n'est pas prêt. On gare après le trait."),
            (N, "Victorino recule. Il essuie une roue du bout du doigt."),
            (M, "Le bleu a séché. Le camion peut devenir le hangar."),
            (N, "Le bateau rejoint le quai dessiné, pile sous la benne."),
            (E, "Le hangar est fermé. Personne ne roule sur la ligne."),
            (N, "Une virgule bleue reste sur une roue, comme un phare."),
        ),
        S(
            (N, "Le tapis a séché. Il reste un rond plus foncé, honnête."),
            (P, "On t'écoute : le quai, puis le hangar."),
            (E, "Le camion a attendu le trait, et le bateau a un hangar."),
            (M, "Merci d'avoir reculé tes roues."),
            (N, "Les moufles chaudes font deux petites montagnes bleues."),
            (N, "Le bateau dort sous la benne, nez vers le quai dessiné."),
            (N, "La virgule bleue sur la roue ne part plus."),
        ),
        "camion,crayon",
        "radiateur,roue",
        "hangar",
    )
    data[("tapis", "dessin", "gobelet")] = (
        S(
            (N, "Victorino veut remplir le gobelet jusqu'au trait bleu de la coque."),
            (N, "Il verse trop. L'eau dépasse la ligne, d'un souffle."),
            (E, "C'est trop !"),
            (M, "On attend, on reprend avec le gobelet, on enlève un peu."),
            (N, "Victorino attend que les ronds s'arrêtent."),
            (N, "Il puise, tout lent, jusqu'à ce que l'eau touche le bleu."),
            (P, "Pile à la ligne. Ton port a la bonne hauteur."),
            (N, "Le bateau entre dans le jaune, voile au-dessus du trait."),
            (N, "Une goutte reste sur le gobelet, puis glisse, sans tomber."),
        ),
        S(
            (N, "Le zinc est vide. La serviette a l'air d'une plage pâle."),
            (M, "Raconte la ligne, et le trop d'eau, et le juste."),
            (E, "J'ai retiré l'eau jusqu'au bleu, et le bateau a son port."),
            (P, "Nous t'avons vu corriger, sans te presser."),
            (N, "Les moufles sèches sentent le radiateur, un peu de fer chaud."),
            (N, "Le bateau tient dans le gobelet, ligne bleue au ras."),
            (N, "Le crayon bleu a une mine usée, fière."),
        ),
        "gobelet,crayon",
        "radiateur,eau",
        "ligne",
    )

    # TABLE + HISTOIRE
    data[("table", "histoire", "doudou")] = (
        S(
            (N, "Victorino hisse le doudou sur une chaise, face au plat."),
            (E, "Toi, tu regardes l'île, comme dans le livre."),
            (N, "Il raconte trop fort pendant que maman tourne la page."),
            (N, "Le doudou penche. Une patte frôle l'eau."),
            (P, "Le spectateur attend la fin de la page, puis il s'assoit."),
            (N, "Victorino redresse le doudou. Il se tait."),
            (M, "L'île d'orange est au bord. Ton bateau peut tourner."),
            (N, "Le bateau contourne la pelure et s'amarre à la patte."),
            (N, "Le doudou, sur la chaise, a vu tout le tour."),
        ),
        S(
            (N, "Le soir, l'orange a disparu. Il reste son parfum sur le bois."),
            (M, "On t'écoute : l'île, puis le spectateur."),
            (E, "Le doudou a regardé, et le bateau a tourné autour de l'orange."),
            (P, "La page a eu sa fin, et le tour aussi."),
            (N, "Les moufles, près du radiateur, sont deux coques chaudes."),
            (N, "Le bateau sèche contre la patte, sur la chaise."),
            (N, "Une miette d'orange orpheline brille sur la table."),
        ),
        "doudou,orange",
        "radiateur,chaise",
        "spectateur",
    )
    data[("table", "histoire", "camion")] = (
        S(
            (N, "Victorino pose le camion comme un livreur, autour du plat."),
            (E, "Il livre le bateau à l'île, comme sur la carte !"),
            (N, "Le camion heurte le livre. Une page se plie."),
            (M, "La carte d'abord, puis la livraison."),
            (N, "Victorino recule. Maman aplatit la page."),
            (N, "Le livre est à l'abri. Les roues repartent, plus lentes."),
            (N, "Le bateau voyage dans la benne, puis rejoint l'eau près de l'île."),
            (P, "Livraison faite. La page n'a plus de pli."),
            (N, "Une goutte sur le toit du camion s'arrête, puis tombe au plat."),
        ),
        S(
            (N, "La table est essuyée. Le bois retrouve ses veines."),
            (P, "Raconte la livraison, depuis la page pliée."),
            (E, "Le camion a attendu la carte, puis il a livré le bateau."),
            (M, "Merci d'avoir reculé tes roues."),
            (N, "Les moufles sèches pendent, paires, comme deux sacs."),
            (N, "Le bateau rentre au garage, dans la benne, près du sel."),
            (N, "Le livre est fermé, page plate, loin des taches."),
        ),
        "camion,pages",
        "radiateur,roue",
        "livraison",
    )
    data[("table", "histoire", "gobelet")] = (
        S(
            (N, "Victorino veut verser une rivière autour de l'île d'orange."),
            (N, "Un peu de jus se mêle à l'eau. Le plat devient trouble."),
            (E, "Ce n'est plus la rivière du livre."),
            (P, "On attend. Je change l'eau, tu verses après."),
            (N, "Victorino tient le gobelet, sans pencher."),
            (N, "Papa vide, puis remplit. L'eau redevient claire."),
            (M, "Maintenant, un filet, comme le dessin."),
            (N, "Le bateau suit le filet, contourne l'île, entre dans le jaune."),
            (N, "L'orange reste une île propre, au bord."),
        ),
        S(
            (N, "La casserole de pluie est vide. Il reste une odeur d'écorce."),
            (M, "Dis-nous le jus, puis l'eau claire."),
            (E, "J'ai attendu l'eau propre, et le bateau a eu sa rivière."),
            (P, "Nous t'avons vu ne pas verser trop tôt."),
            (N, "Les moufles, chaudes, ont repris leur bleu profond."),
            (N, "Le bateau flotte dans le gobelet, face à l'île vide."),
            (N, "Une pelure sèche sur l'assiette, comme un rivage."),
        ),
        "gobelet,orange",
        "radiateur,eau",
        "rivière",
    )

    # TABLE + CHANSON
    data[("table", "chanson", "doudou")] = (
        S(
            (N, "Victorino fait hocher l'oreille du doudou à chaque coup de bois."),
            (E, "Il dirige l'orchestre !"),
            (N, "Il chante par-dessus papa. Les trois coups se mélangent."),
            (M, "Le chef d'orchestre écoute d'abord, puis il dirige."),
            (N, "Victorino ferme la bouche. L'oreille du doudou attend."),
            (N, "Trois coups clairs. Au troisième, l'oreille s'incline."),
            (N, "Le bateau part et s'amarre sous le museau, pile au rythme."),
            (P, "Ton chef a dirigé après la mesure, pas pendant."),
            (N, "La carafe a cessé de vibrer."),
        ),
        S(
            (N, "Les cuillères sont silencieuses, dans leur tiroir."),
            (P, "On t'écoute : les trois coups, puis le museau."),
            (E, "Le doudou a dirigé au troisième, et le bateau s'est amarré."),
            (M, "L'orchestre a eu sa mesure entière."),
            (N, "Les moufles sèches tapent un tout petit tic, contre le métal."),
            (N, "Le bateau sèche sous le museau, sur la nappe."),
            (N, "Une oreille garde le souvenir des trois coups, un pli."),
        ),
        "doudou,tapotement",
        "radiateur,tissu",
        "orchestre",
    )
    data[("table", "chanson", "camion")] = (
        S(
            (N, "Victorino fait d'une roue un métronome, contre le bois."),
            (N, "Il accélère. Le plat glisse vers le bord de la table."),
            (P, "Le métronome suit mes coups, pas l'inverse."),
            (N, "Victorino arrête la roue. Il écoute les trois sourds."),
            (E, "Un. Deux. Trois. Maintenant la remorque."),
            (N, "Le camion escorte le bateau autour du plat, au pas."),
            (M, "La mesure a tenu. Le plat aussi."),
            (N, "Le bateau entre sous la benne, au troisième écho."),
            (N, "Une miette roule, puis s'arrête, comme une île morte."),
        ),
        S(
            (N, "La table ne vibre plus. Il reste une ronde d'eau essuyée."),
            (M, "Raconte le métronome, depuis le trop vite."),
            (E, "La roue a ralenti, et le bateau a suivi le troisième coup."),
            (P, "Merci d'avoir arrêté tes roues."),
            (N, "Les moufles, au salon, sont sèches comme du pain chaud."),
            (N, "Le bateau rentre au hangar, benne baissée près de la salière."),
            (N, "La miette d'île a disparu dans un torchon."),
        ),
        "camion,tapotement",
        "radiateur,roue",
        "métronome",
    )
    data[("table", "chanson", "gobelet")] = (
        S(
            (N, "Victorino frappe le gobelet : ding, puis il verse."),
            (N, "Le ding et l'eau partent ensemble. Le plat déborde d'un filet."),
            (M, "La cloche d'abord. L'eau ensuite."),
            (N, "Victorino essuie le filet. Il attend le silence jaune."),
            (P, "Trois coups de table, un ding, puis ton filet."),
            (N, "Le rythme se pose. Personne ne parle."),
            (N, "Le filet pousse le bateau jusqu'au gobelet, sans déborder."),
            (E, "La cloche a fini. Le port est plein, juste assez."),
            (N, "Une perle d'eau tient au bord du jaune, puis rentre."),
        ),
        S(
            (N, "Le bois de la table a séché, une marée basse."),
            (P, "Dis-nous le ding, puis le filet, dans l'ordre."),
            (E, "J'ai versé après la cloche, et le bateau a son port."),
            (M, "Nous t'avons entendu respecter l'ordre."),
            (N, "Les moufles chaudes ont un pompon un peu dur, séché."),
            (N, "Le bateau tient dans le gobelet, près de la carafe."),
            (N, "Le ding n'existe plus, mais la table s'en souvient."),
        ),
        "gobelet,tapotement",
        "radiateur,cloche",
        "ding",
    )

    # TABLE + DESSIN
    data[("table", "dessin", "doudou")] = (
        S(
            (N, "Le crayon dépose un point bleu sur le nez du doudou, par erreur."),
            (E, "Oh. Un grade de capitaine."),
            (N, "Victorino veut lancer malgré le trait inachevé sur la coque."),
            (M, "On essuie le nez, on finit la ligne, puis on part."),
            (N, "Victorino attend. Maman passe un coin de torchon."),
            (N, "Le point devient plus pâle. La ligne de la coque se ferme."),
            (N, "Le bateau s'amarre sous le nez, pile au bleu."),
            (P, "Ton capitaine a un grade, et un quai net."),
            (N, "Le torchon garde un petit ciel, une tache ronde."),
        ),
        S(
            (N, "La lampe de la table fait un rond jaune sur le bois."),
            (M, "Raconte le nez bleu, puis le quai."),
            (E, "Le doudou a un grade, et le bateau s'est arrêté à la ligne."),
            (P, "Tu as laissé finir le trait."),
            (N, "Les moufles, au radiateur, sont deux drapeaux bleus au repos."),
            (N, "Le bateau sèche sous le nez, un point pâle pour phare."),
            (N, "Le torchon sèche aussi, petit ciel oublié."),
        ),
        "doudou,crayon",
        "radiateur,tissu",
        "grade",
    )
    data[("table", "dessin", "camion")] = (
        S(
            (N, "Maman dessine un port sur une serviette de table, un croissant."),
            (N, "Victorino y pousse le camion. Le crayon bave sous une roue."),
            (P, "Le port se gare tout seul, quand le trait a séché."),
            (N, "Victorino soulève le camion. Il compte jusqu'à trois."),
            (M, "Le croissant est net. Le hangar peut s'installer."),
            (N, "Le bateau rejoint le croissant, sous la benne, sans bavure."),
            (E, "Personne ne roule sur le port, maintenant."),
            (N, "Une virgule bleue orne le pare-chocs, volontaire cette fois."),
            (N, "La salière fait office de phare, au bout du bois."),
        ),
        S(
            (N, "La serviette de table sèche sur le dossier d'une chaise."),
            (P, "On t'écoute : le croissant, puis le hangar."),
            (E, "Le camion a attendu le port, et le bateau s'y est rangé."),
            (M, "Merci d'avoir compté jusqu'à trois."),
            (N, "Les moufles chaudes ont l'odeur du pain, un peu."),
            (N, "Le bateau dort dans la benne, nez vers la salière."),
            (N, "Le croissant bleu tient, un port miniature."),
        ),
        "camion,crayon",
        "radiateur,roue",
        "croissant",
    )
    data[("table", "dessin", "gobelet")] = (
        S(
            (N, "Victorino aligne l'eau du gobelet sur la ligne bleue de la coque."),
            (N, "Il en met trop. Le bleu disparaît sous un trop-plein."),
            (E, "Je ne vois plus le quai."),
            (M, "On attend les ronds, puis on retire, jusqu'au bleu."),
            (N, "Victorino pose le gobelet. Il regarde l'eau se taire."),
            (N, "Il puise. La ligne reparaît, un fil."),
            (P, "Le quai est visible. Ton port a la bonne mesure."),
            (N, "Le bateau entre, voile sèche, coque au ras du bleu."),
            (N, "Une goutte d'orange, loin, ne se mêle plus."),
        ),
        S(
            (N, "Le plat est égoutté. Il reste un cercle plus clair sur le bois."),
            (M, "Raconte le trop-plein, puis le fil bleu."),
            (E, "J'ai retiré l'eau, et le bateau a vu son quai."),
            (P, "Nous t'avons vu attendre les ronds."),
            (N, "Les moufles sèches font un bruit de laine, quand on les plie."),
            (N, "Le bateau tient dans le gobelet, ligne visible, fière."),
            (N, "Le crayon repose près du sel, mine vers le mur."),
        ),
        "gobelet,crayon",
        "radiateur,eau",
        "trop-plein",
    )

    # FENETRE + HISTOIRE
    data[("fenetre", "histoire", "doudou")] = (
        S(
            (N, "Victorino installe le doudou contre la vitre, face à la pluie."),
            (E, "Toi, tu vois les deux bateaux : le livre, et le vrai."),
            (N, "Il pointe trop vite. Le doudou glisse vers le bol."),
            (M, "Le témoin s'assoit après la page, pas pendant."),
            (N, "Victorino rattrape l'oreille. Il attend la fin de l'image."),
            (N, "Maman baisse le livre. Les deux voiles se répondent."),
            (N, "Le bateau du bol s'appuie à la patte, voile plus haute."),
            (P, "Ton témoin a vu le vrai, et le dessiné."),
            (N, "Une buée de nez s'efface sur la vitre, tout rond."),
        ),
        S(
            (N, "La gouttière se tait. Il reste des perles aux bords du toit."),
            (M, "Raconte les deux voiles, depuis le glissement."),
            (E, "Le doudou a comparé, et le vrai bateau a levé sa voile."),
            (P, "Le témoin a attendu la page."),
            (N, "Les moufles, au salon, sont sèches, un peu plus petites."),
            (N, "Le bateau sèche contre la patte, face à la vitre noire."),
            (N, "Le livre est fermé, les deux voiles rangées dans la tête."),
        ),
        "doudou,vitre",
        "radiateur,tissu",
        "témoin",
    )
    data[("fenetre", "histoire", "camion")] = (
        S(
            (N, "Victorino place le camion en barrière, au bord du rebord."),
            (E, "Comme ça, le bateau ne tombe pas, même si le vent pousse."),
            (N, "Papa veut ranger le camion pendant qu'il parle du loquet."),
            (N, "Victorino touche sa manche, sans crier."),
            (E, "Quand tu as fini le loquet, le camion garde le bord."),
            (P, "Oui. Le loquet est fait. Ta barrière reste."),
            (N, "Le bateau voyage dans le bol, sans approcher le vide."),
            (M, "La page du livre montre un quai. Toi, tu as un camion-quai."),
            (N, "Une roue touche presque le dehors, et s'arrête."),
        ),
        S(
            (N, "Le loquet est fermé. Le vent gratte, sans entrer."),
            (P, "On t'écoute : la manche, puis la barrière."),
            (E, "Le camion a gardé le bord, et le bateau n'est pas tombé."),
            (M, "Merci d'avoir touché la manche, au lieu de crier."),
            (N, "Les moufles chaudes reposent, paires, sous le tic."),
            (N, "Le bateau sèche derrière le camion, loin du vide."),
            (N, "Le rebord a une trace de roue, un garde-fou minuscule."),
        ),
        "camion,loquet",
        "radiateur,roue",
        "barrière",
    )
    data[("fenetre", "histoire", "gobelet")] = (
        S(
            (N, "Victorino tend le gobelet sous la gouttière, pour le fleuve du livre."),
            (N, "Le gobelet déborde. Une goutte atteint le coin de la page."),
            (M, "On rentre le livre, on attend une goutte, pas dix."),
            (N, "Victorino recule le jaune. Maman sauve la page."),
            (N, "Une seule goutte tombe. Il la cueille, pile."),
            (N, "Il verse ce peu dans le bol. Le bateau avance d'un souffle."),
            (P, "Ton fleuve a la taille d'une goutte, comme il faut."),
            (E, "Le livre est sec. Le vrai bateau a bougé."),
            (N, "La gouttière continue, plus loin, sans eux."),
        ),
        S(
            (N, "La vitre a séché, sauf un coin bas, un peu flou."),
            (M, "Dis-nous les dix gouttes, puis la seule."),
            (E, "J'ai cueilli une goutte, et le bateau a avancé, sans mouiller le livre."),
            (P, "Nous t'avons vu reculer le gobelet."),
            (N, "Les moufles sèches ont l'odeur du radiateur, un peu de fer."),
            (N, "Le bateau sèche dans le gobelet, sous le rebord."),
            (N, "Le livre est au sec, sur la commode, coin net."),
        ),
        "gobelet,gouttiere",
        "radiateur,pages",
        "goutte",
    )

    # FENETRE + CHANSON
    data[("fenetre", "chanson", "doudou")] = (
        S(
            (N, "Victorino colle l'oreille du doudou contre le tuyau de gouttière."),
            (E, "Il chante avec la note longue."),
            (N, "Il lance le bateau sur une note courte. Le bol penche."),
            (P, "Le chœur attend la longue. Tu l'as sous l'oreille ?"),
            (N, "Victorino écoute à travers le gris du doudou."),
            (N, "La note longue arrive, grave, dans l'oreille de tissu."),
            (N, "Au milieu de la note, le bateau part et s'amarre à la patte."),
            (M, "Ton chœur a tenu la mesure du toit."),
            (N, "Le bol se recale. L'eau n'a plus peur."),
        ),
        S(
            (N, "Le tuyau s'endort. Il reste un goutte-à-goutte, très loin."),
            (P, "Chante-nous la courte, puis la longue."),
            (E, "Le doudou a entendu la longue, et le bateau est parti avec."),
            (M, "Ton chœur n'a pas sauté la mesure."),
            (N, "Les moufles, sèches, ont un pompon un peu raide."),
            (N, "Le bateau sèche contre l'oreille, pleine de tuyau."),
            (N, "La vitre garde un halo, là où l'oreille s'était collée."),
        ),
        "doudou,gouttiere",
        "radiateur,tissu",
        "chœur",
    )
    data[("fenetre", "chanson", "camion")] = (
        S(
            (N, "Victorino attend la note longue pour faire remorquer le bateau."),
            (N, "Il avance le camion trop tôt. Une roue glisse vers le vide."),
            (M, "Les roues écoutent le toit, puis elles tirent."),
            (N, "Victorino recule. Papa garde une main près du rebord."),
            (N, "La note longue s'installe. Les roues avancent d'un cran."),
            (N, "Le bateau suit, ficelle imaginaire, jusqu'au milieu du bol."),
            (P, "Ta remorque a pris la note, pas le vide."),
            (E, "On part avec le toit, pas contre."),
            (N, "Une goutte frappe le toit du camion, puis rejoint le bol."),
        ),
        S(
            (N, "Le rebord est sec, sauf sous le camion, une ombre humide."),
            (M, "Raconte la roue vers le vide, puis la note."),
            (E, "Le camion a reculé, puis il a tiré sur la longue."),
            (P, "Merci d'avoir reculé avant le vide."),
            (N, "Les moufles chaudes sont rentrées dans le panier à laine."),
            (N, "Le bateau sèche dans la benne, face à la gouttière close."),
            (N, "Le loquet garde le silence, un petit métal."),
        ),
        "camion,gouttiere",
        "radiateur,roue",
        "remorque",
    )
    data[("fenetre", "chanson", "gobelet")] = (
        S(
            (N, "Victorino veut verser sur la note longue, un accompagnement."),
            (N, "Il penche sur la courte. Le bol reçoit trop, d'un coup."),
            (P, "La courte est un silence. On verse sur la longue."),
            (N, "Victorino redresse le jaune. Il écoute le tuyau."),
            (N, "La note longue s'étire. Il verse un filet, avec elle."),
            (N, "Le bateau avance, porté par la musique du toit."),
            (M, "Ton gobelet a chanté juste, cette fois."),
            (E, "La courte, je la garde pour me taire."),
            (N, "Une dernière perle tient au gobelet, puis choisit le bol."),
        ),
        S(
            (N, "La pluie a fini sa chanson. Le village redevient net."),
            (P, "Dis-nous la courte, puis la longue, puis le filet."),
            (E, "J'ai versé avec la longue, et le bateau a avancé."),
            (M, "Nous t'avons vu redresser le gobelet."),
            (N, "Les moufles sèches attendent près de la porte, pour plus tard."),
            (N, "Le bateau sèche dans le jaune, sous la gouttière vide."),
            (N, "Le bol en bois sent le toit, un peu."),
        ),
        "gobelet,gouttiere",
        "radiateur,eau",
        "filet",
    )

    # FENETRE + DESSIN
    data[("fenetre", "dessin", "doudou")] = (
        S(
            (N, "Un trait de doigt reste sur la vitre, à côté du doudou."),
            (E, "C'est une fenêtre pour le capitaine."),
            (N, "Victorino veut partir pendant que maman finit le quai bleu."),
            (M, "Le capitaine attend le quai, même s'il a sa fenêtre."),
            (N, "Victorino pose le bateau. Le doudou regarde le doigt sur le verre."),
            (N, "Le trait de coque se ferme, net, au-dessus de l'eau."),
            (N, "Le bateau s'amarre à la patte, face à la petite fenêtre."),
            (P, "Deux fenêtres : la vraie, et celle du doigt."),
            (N, "La buée entoure le trait, comme un cadre."),
        ),
        S(
            (N, "La buée est partie. Le trait de doigt est devenu un fantôme."),
            (M, "Raconte la fenêtre du capitaine, puis le quai."),
            (E, "Le doudou a sa fenêtre, et le bateau a attendu le bleu."),
            (P, "Le quai a eu le temps de se fermer."),
            (N, "Les moufles, sèches, sont rentrées dans le tiroir du banc."),
            (N, "Le bateau sèche contre la patte, face au verre noir."),
            (N, "Le fantôme du doigt reste, à peine, au ras du rebord."),
        ),
        "doudou,crayon",
        "radiateur,vitre",
        "fenêtre",
    )
    data[("fenetre", "dessin", "camion")] = (
        S(
            (N, "Victorino pose le camion sur la feuille, pour tenir le papier."),
            (N, "Le vent pousse. Le camion roule. Le crayon dérape sur la coque."),
            (P, "On attend la rafale, on recale le poids, puis le trait."),
            (N, "Victorino retient les roues. La rafale passe."),
            (M, "Maintenant, le poids tient. Je finis le quai."),
            (N, "Le trait bleu se pose, droit, pendant que le camion fait presse-papier."),
            (N, "Le bateau part dans le bol, et revient sous la benne."),
            (E, "Le poids a écouté le vent, avant de peser."),
            (N, "Une virgule de mine reste sur le toit rouge, un accident sage."),
        ),
        S(
            (N, "Le vent a cessé. Les volets ne bougent plus."),
            (P, "On t'écoute : la rafale, puis le presse-papier."),
            (E, "Le camion a attendu le vent, et le bateau a un quai droit."),
            (M, "Merci d'avoir retenu les roues."),
            (N, "Les moufles chaudes sont deux coques, dans le panier."),
            (N, "Le bateau sèche sous la benne, virgule bleue pour phare."),
            (N, "Le rebord a perdu son courant d'air, enfin."),
        ),
        "camion,crayon",
        "radiateur,roue",
        "presse-papier",
    )
    data[("fenetre", "dessin", "gobelet")] = (
        S(
            (N, "Victorino compare l'eau du gobelet au trait bleu de la coque."),
            (N, "Le vent pousse sa main. Un trop-plein menace le rebord."),
            (M, "On attend le vent, on verse ensuite, jusqu'au bleu."),
            (N, "Victorino recule le jaune. Une rafale s'en va."),
            (N, "Il verse un filet. L'eau du bol rejoint pile la ligne."),
            (N, "Le bateau entre dans le gobelet, voile au-dessus du quai."),
            (P, "Ton niveau est juste. Le dehors n'a rien pris."),
            (E, "Le vent a parlé. Après, c'était mon tour."),
            (N, "Une perle tient au bois du bol, puis choisit de rester."),
        ),
        S(
            (N, "Le village a séché. Seul le toit garde quelques perles."),
            (M, "Dis-nous le vent, puis le filet, puis la ligne."),
            (E, "J'ai versé après le vent, et le bateau a vu son bleu."),
            (P, "Nous t'avons vu reculer, puis verser."),
            (N, "Les moufles sèches gardent un peu de pluie, au chaud."),
            (N, "Le bateau tient dans le jaune, sous le rebord tranquille."),
            (N, "Le bol en bois sent le toit, et plus le vent."),
        ),
        "gobelet,crayon",
        "radiateur,eau",
        "niveau",
    )

    if len(data) != 27:
        raise SystemExit(f"t3_scenes {len(data)}")
    return data


if __name__ == "__main__":
    build()
