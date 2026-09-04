#!/usr/bin/env python3
"""Génère merged.json pour TREE-DIF-004 et TREE-DIF-005 (texte seulement)."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FORBIDDEN_SUB = (
    "On va apprendre",
    "Voici le geste",
    "Il était une fois",
    "Ceci est l'histoire",
    "papa sourit",
    "maman sourit",
    "maman est là",
    "papa est là",
)
FORBIDDEN_NAMES = (
    "Adam",
    "Iris",
    "Lina",
    "Nora",
    "Lucas",
    "Céline",
    "Celine",
    "Luca",
    "Noé",
    "Noe",
    "Jules",
    "Tom",
    "Léa",
    "Lea",
    "Sami",
)


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    script = "\n".join(f"{role}|{phrase}" for role, phrase in lines)
    text = " ".join(phrase for _, phrase in lines)
    return text, script


def apply_chunk(src: dict, lines: list[tuple[str, str]], sons: str | None = None) -> dict:
    text, script = pack(lines)
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    if sons is None:
        out["sons"] = src.get("sons") or ""
    else:
        out["sons"] = sons
    return out


def wc(phrase: str) -> int:
    return len(phrase.replace("'", " ").replace("’", " ").split())


def check_phrases(story_id: str, by: dict[str, list[tuple[str, str]]], max_words: int) -> None:
    bad: list[str] = []
    for cid, lines in by.items():
        for role, ph in lines:
            if "|" in ph:
                bad.append(f"{cid} pipe in phrase: {ph}")
            n = wc(ph)
            if n > max_words:
                bad.append(f"{cid} {n}w {role}|{ph}")
            if not ph.endswith((".", "?", "!")):
                bad.append(f"{cid} no end punct {role}|{ph}")
    if bad:
        raise SystemExit(f"{story_id} phrases:\n" + "\n".join(bad[:50]))


def check_text(story_id: str, by: dict[str, list[tuple[str, str]]], extra_forbid: tuple[str, ...] = ()) -> None:
    blob = " ".join(ph for lines in by.values() for _, ph in lines)
    for s in FORBIDDEN_SUB:
        if s.lower() in blob.lower():
            raise SystemExit(f"{story_id} interdit: {s}")
    for name in FORBIDDEN_NAMES + extra_forbid:
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{story_id} nom interdit: {name}")


def sent(extra: str) -> list[tuple[str, str]]:
    parts = [p.strip() for p in extra.split(". ") if p.strip()]
    return [("narrateur", p if p.endswith((".", "?", "!")) else p + ".") for p in parts]


def write_story(
    story_id: str,
    meta: dict,
    by_id: dict[str, list[tuple[str, str]]],
    sons_map: dict[str, str],
    max_words: int,
    extra_forbid: tuple[str, ...] = (),
) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:8]} extra={extra[:8]}")
    check_phrases(story_id, by_id, max_words)
    check_text(story_id, by_id, extra_forbid)
    chunks = []
    for c in source["chunks"]:
        cid = c["chunk_id"]
        chunks.append(apply_chunk(c, by_id[cid], sons_map.get(cid)))
    merged = dict(source)
    merged.update(meta)
    merged["chunks"] = chunks
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def story_004() -> None:
    jeux = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    aliments = {"P0001": "pomme", "P0002": "yaourt", "P0003": "pain"}
    animaux = {"P0001": "chat", "P0002": "chien", "P0003": "poule"}
    jeu_np = {"cubes": "les cubes", "livre": "le livre", "dinette": "la dînette"}
    alim_np = {"pomme": "la pomme", "yaourt": "le yaourt", "pain": "le pain"}
    anim_np = {"chat": "le chat", "chien": "le chien", "poule": "la poule"}

    jeu_l1 = {
        "cubes": [
            ("narrateur", "Raphaël pose les cubes sur la table."),
            ("narrateur", "Un cube rouge sent le pin."),
            ("narrateur", "Un cube bleu fait clic, tout doux."),
            ("narrateur", "Nino les regarde, sans un mot."),
            ("narrateur", "Ses mains restent sur ses genoux."),
            ("narrateur", "Raphaël a envie de demander."),
            ("narrateur", "Il attend, tout calme."),
            ("enfant-m", "Je lui tends le cube rouge."),
            ("narrateur", "Nino prend le cube."),
            ("narrateur", "Il le pose, tout droit."),
            ("maman", "Bravo, Raphaël."),
            ("maman", "Tu as su attendre."),
            ("papa", "On peut tendre un jouet."),
            ("papa", "On ne force pas la parole."),
            ("papa", "On peut jouer ensemble."),
            ("narrateur", "Deux cubes font une petite tour."),
            ("narrateur", "Nino ajoute le cube bleu."),
            ("narrateur", "La tour tient, tout silencieuse."),
        ],
        "livre": [
            ("narrateur", "Raphaël ouvre le livre à images."),
            ("narrateur", "La page sent le papier, un peu sec."),
            ("narrateur", "Un chat dessiné lève la patte."),
            ("narrateur", "Nino touche le bord de la page."),
            ("narrateur", "Il ne dit rien."),
            ("narrateur", "Raphaël attend, les mains à plat."),
            ("enfant-m", "Je lui tends le livre."),
            ("narrateur", "Nino prend le livre."),
            ("narrateur", "Il caresse l'image, tout lentement."),
            ("papa", "On peut attendre."),
            ("papa", "On peut tendre un jouet."),
            ("maman", "On ne force pas la parole."),
            ("maman", "On peut jouer ensemble."),
            ("narrateur", "Une page tourne, tout seule presque."),
            ("enfant-m", "J'attends encore."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Nino sourit, sans parler."),
        ],
        "dinette": [
            ("narrateur", "Raphaël sort la dînette."),
            ("narrateur", "Une tasse cliquette, tout creux."),
            ("narrateur", "Une cuillère miniature est encore tiède."),
            ("narrateur", "Nino s'assoit près de la nappe."),
            ("narrateur", "Il regarde la petite casserole."),
            ("narrateur", "Raphaël attend un petit moment."),
            ("enfant-m", "Je lui tends la tasse."),
            ("narrateur", "Nino prend la tasse."),
            ("narrateur", "Il la pose devant lui."),
            ("maman", "On peut attendre."),
            ("maman", "On peut tendre un jouet."),
            ("papa", "On ne force pas la parole."),
            ("papa", "On n'imite pas."),
            ("maman", "On peut jouer ensemble."),
            ("narrateur", "Raphaël verse de l'air, tout sérieux."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "Tu as tendu un jouet."),
            ("narrateur", "La tasse reste entre les deux."),
        ],
    }

    q = {
        "cubes": [
            ("narrateur", "Nino parle peu."),
            ("maman", "On fait quoi ?"),
        ],
        "livre": [
            ("narrateur", "Nino touche la page."),
            ("papa", "On attend, ou on tend un jouet ?"),
        ],
        "dinette": [
            ("narrateur", "Nino tient la tasse."),
            ("maman", "On attend sa parole ?"),
        ],
    }

    conf = {
        "cubes": [
            ("papa", "Oui."),
            ("papa", "On attend."),
            ("papa", "On tend un jouet."),
            ("narrateur", "Raphaël souffle un peu."),
            ("narrateur", "Le cube rouge reste dans la main de Nino."),
            ("enfant-m", "J'ai attendu."),
            ("maman", "Bravo, Raphaël."),
            ("maman", "C'est du bon travail."),
            ("papa", "On ne force pas la parole."),
            ("papa", "On peut jouer ensemble."),
        ],
        "livre": [
            ("maman", "Oui."),
            ("maman", "On attend."),
            ("maman", "On tend un jouet."),
            ("narrateur", "La page reste ouverte, tout calme."),
            ("enfant-m", "Je tends le livre."),
            ("papa", "Bravo."),
            ("papa", "Tu as su attendre."),
            ("maman", "On ne force pas la parole."),
            ("narrateur", "Nino caresse encore le chat dessiné."),
        ],
        "dinette": [
            ("papa", "Oui."),
            ("papa", "On attend."),
            ("papa", "On tend un jouet."),
            ("narrateur", "La petite tasse cliquette encore."),
            ("enfant-m", "J'attends."),
            ("maman", "Bravo."),
            ("maman", "On ne force pas la parole."),
            ("papa", "On peut jouer ensemble."),
            ("narrateur", "Nino tient la cuillère, tout silencieux."),
        ],
    }

    alim_scene = {
        "pomme": [
            ("narrateur", "Papa coupe une pomme jaune."),
            ("narrateur", "La peau est lisse, un peu froide."),
            ("narrateur", "Une goutte de jus brille sur la table."),
            ("papa", "Tu veux un quartier, Nino ?"),
            ("narrateur", "Nino regarde la pomme."),
            ("narrateur", "Il ne dit rien."),
            ("narrateur", "Raphaël attend."),
            ("enfant-m", "Je lui tends le quartier."),
            ("narrateur", "Nino prend la pomme."),
            ("narrateur", "Il croque, tout petit."),
            ("maman", "On peut attendre."),
            ("maman", "On peut tendre un jouet."),
            ("papa", "On ne force pas la parole."),
            ("papa", "On peut jouer ensemble."),
            ("maman", "Bravo, Raphaël."),
            ("maman", "Tu as tendu, sans presser."),
        ],
        "yaourt": [
            ("narrateur", "Maman sort un yaourt du saladier froid."),
            ("narrateur", "Le pot est lisse, un peu mouillé."),
            ("narrateur", "Une cuillère tape le bord."),
            ("maman", "Le yaourt est là, Nino."),
            ("narrateur", "Nino tapote le pot."),
            ("narrateur", "Raphaël attend, les mains sages."),
            ("enfant-m", "Je lui tends la cuillère."),
            ("narrateur", "Nino prend la cuillère."),
            ("papa", "On peut attendre."),
            ("papa", "On peut tendre un jouet."),
            ("maman", "On ne force pas la parole."),
            ("maman", "On peut jouer ensemble."),
            ("papa", "Bravo."),
            ("papa", "Tu as su attendre."),
            ("narrateur", "Une goutte blanche reste sur la nappe."),
        ],
        "pain": [
            ("narrateur", "Papa tend un morceau de pain."),
            ("narrateur", "La croûte est encore tiède."),
            ("narrateur", "Ça sent le four, tout doux."),
            ("papa", "Tu le sens, Nino ?"),
            ("narrateur", "Nino approche le pain."),
            ("narrateur", "Il ne parle pas."),
            ("narrateur", "Raphaël attend la fin du silence."),
            ("enfant-m", "Je lui tends le pain."),
            ("narrateur", "Nino prend le morceau."),
            ("maman", "On peut attendre."),
            ("maman", "On peut tendre un jouet."),
            ("papa", "On ne force pas la parole."),
            ("papa", "On peut jouer ensemble."),
            ("maman", "Bravo, Raphaël."),
            ("narrateur", "Une miette reste près du cube."),
        ],
    }

    extra_jeu_alim = {
        ("cubes", "pomme"): "Un cube attrape un reflet de pomme.",
        ("cubes", "yaourt"): "Un cube blanc colle un peu de yaourt.",
        ("cubes", "pain"): "Une miette de pain dort près d'un cube.",
        ("livre", "pomme"): "Une goutte de jus reste au bord de la page.",
        ("livre", "yaourt"): "Le livre est un peu loin du pot froid.",
        ("livre", "pain"): "Une miette marque la page, tout doux.",
        ("dinette", "pomme"): "La petite assiette est près du quartier.",
        ("dinette", "yaourt"): "La petite cuillère tremble près du pot.",
        ("dinette", "pain"): "La dînette sent encore le pain chaud.",
    }

    anim_open = {
        "chat": [
            ("narrateur", "Le chat de la maison s'étire sur la chaise."),
            ("narrateur", "Son dos est chaud, tout soyeux."),
            ("narrateur", "Il fait un petit ronron."),
            ("maman", "Le chat aime le calme, lui aussi."),
            ("narrateur", "Nino tend un doigt, tout lentement."),
            ("narrateur", "Raphaël attend."),
            ("enfant-m", "Je lui tends le jouet souris."),
            ("narrateur", "Nino pose le jouet près du chat."),
            ("papa", "On peut attendre."),
            ("papa", "On peut tendre un jouet."),
            ("maman", "On ne force pas la parole."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "Tu as su attendre."),
        ],
        "chien": [
            ("narrateur", "Le chien gratte doucement la porte."),
            ("narrateur", "Ses poils sentent l'herbe mouillée."),
            ("narrateur", "Il fait un wouaf, tout amical."),
            ("papa", "Le chien est content, tout simplement."),
            ("narrateur", "Nino recule un peu, puis avance."),
            ("narrateur", "Raphaël attend, tout près."),
            ("enfant-m", "Je lui tends la balle molle."),
            ("narrateur", "Nino pose la balle au sol."),
            ("maman", "On peut attendre."),
            ("maman", "On peut tendre un jouet."),
            ("papa", "On ne force pas la parole."),
            ("maman", "On peut jouer ensemble."),
            ("papa", "Bravo."),
            ("papa", "C'est du bon travail."),
        ],
        "poule": [
            ("narrateur", "La poule picore près du bac, dehors."),
            ("narrateur", "Ses plumes sont rousses, un peu mouillées."),
            ("narrateur", "Elle fait cot cot, tout bas."),
            ("maman", "On la regarde, tout doux."),
            ("narrateur", "Nino s'accroupit, sans un mot."),
            ("narrateur", "Raphaël attend à côté."),
            ("enfant-m", "Je lui tends le seau de grains."),
            ("narrateur", "Nino pose le seau, tout lentement."),
            ("papa", "On peut attendre."),
            ("papa", "On peut tendre un jouet."),
            ("maman", "On ne force pas la parole."),
            ("maman", "On peut jouer ensemble."),
            ("papa", "Bravo, Raphaël."),
            ("papa", "Tu as tendu, sans presser."),
        ],
    }

    extras_l3 = {
        ("cubes", "pomme", "chat"): "Un cube rouge reste près des moustaches.",
        ("cubes", "pomme", "chien"): "Un cube roule jusqu'aux pattes mouillées.",
        ("cubes", "pomme", "poule"): "Un cube jaune brille près des grains.",
        ("cubes", "yaourt", "chat"): "Le chat ignore le pot, tout fier.",
        ("cubes", "yaourt", "chien"): "Le chien renifle le pot, puis s'assoit.",
        ("cubes", "yaourt", "poule"): "La poule picore loin du yaourt froid.",
        ("cubes", "pain", "chat"): "Une miette intéresse le chat, une seconde.",
        ("cubes", "pain", "chien"): "Le chien pose le nez près du pain.",
        ("cubes", "pain", "poule"): "La poule préfère le grain au pain.",
        ("livre", "pomme", "chat"): "Le chat vrai ressemble au chat du livre.",
        ("livre", "pomme", "chien"): "Une page claque, tout petit, près du chien.",
        ("livre", "pomme", "poule"): "La poule du livre a un bec trop rond.",
        ("livre", "yaourt", "chat"): "Le livre reste ouvert sur les genoux calmes.",
        ("livre", "yaourt", "chien"): "Le chien attend, comme Nino, tout sage.",
        ("livre", "yaourt", "poule"): "Une image de poule brille, un peu tachée.",
        ("livre", "pain", "chat"): "Une miette sèche au bord de la page.",
        ("livre", "pain", "chien"): "Le chien écoute le papier, tout curieux.",
        ("livre", "pain", "poule"): "La poule s'éloigne. Le livre reste ouvert.",
        ("dinette", "pomme", "chat"): "La petite tasse est près de la gamelle.",
        ("dinette", "pomme", "chien"): "La casserole miniature sonne près du collier.",
        ("dinette", "pomme", "poule"): "Une petite assiette a une plume collée.",
        ("dinette", "yaourt", "chat"): "Le chat tape la tasse, tout léger.",
        ("dinette", "yaourt", "chien"): "Le chien laisse la dînette tranquille.",
        ("dinette", "yaourt", "poule"): "La poule picore. La tasse cliquette encore.",
        ("dinette", "pain", "chat"): "Le chat se recroqueville près de la nappe.",
        ("dinette", "pain", "chien"): "Le chien s'allonge. La dînette se range.",
        ("dinette", "pain", "poule"): "Une plume rousse reste sur la petite assiette.",
    }

    fin_image = {
        "chat": "Le chat se rendort, tout rond.",
        "chien": "Le chien pose la tête, tout calme.",
        "poule": "La poule rentre sous l'auvent, tout doux.",
    }

    def l3(jeu: str, alim: str, anim: str) -> list[tuple[str, str]]:
        return (
            anim_open[anim]
            + sent(extras_l3[(jeu, alim, anim)])
            + [
                ("narrateur", f"Raphaël a encore {jeu_np[jeu]}."),
                ("narrateur", {
                    "pomme": "Il reste un quartier de pomme.",
                    "yaourt": "Il reste un peu de yaourt.",
                    "pain": "Il reste une croûte de pain.",
                }[alim]),
                ("maman", "On peut attendre."),
                ("papa", "On peut tendre un jouet."),
                ("enfant-m", "J'ai attendu."),
                ("maman", "Bravo."),
                ("papa", "On ne force pas la parole."),
            ]
        )

    def fin(jeu: str, alim: str, anim: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "Merci, papa."),
            ("enfant-m", "Merci, maman."),
            ("maman", "Bravo, Raphaël."),
            ("papa", "Tu as fait du bon travail."),
            ("papa", "Tu as su attendre."),
            ("narrateur", f"Raphaël a joué avec {jeu_np[jeu]}."),
            ("narrateur", f"Nino a pris {alim_np[alim]}, sans parler."),
            ("narrateur", f"Ils ont vu {anim_np[anim]}, tout ensemble."),
            ("narrateur", fin_image[anim]),
            ("narrateur", "L'histoire est finie."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "La gouttière fait un chant, tout fin."),
        ("narrateur", "Des gouttes tapent le zinc, une par une."),
        ("narrateur", "La buée recouvre la vitre de la cuisine."),
        ("narrateur", "Derrière, le village est tout flou."),
        ("narrateur", "La nappe à carreaux sent le savon."),
        ("narrateur", "Une miette de pain dort près du saladier."),
        ("narrateur", "La soupe fume dans la casserole."),
        ("narrateur", "La cuillère en bois goutte, tout lentement."),
        ("narrateur", "Papa coupe le pain, tout près du bord."),
        ("narrateur", "Maman essuie la buée d'un coin de torchon."),
        ("papa", "Tu entends la gouttière, Raphaël ?"),
        ("enfant-m", "Elle fait ploc, papa."),
        ("maman", "La soupe est presque prête."),
        ("narrateur", "Des chaussures mouillées attendent près de la porte."),
        ("narrateur", "Une écharpe goutte encore, sur le carrelage."),
        ("narrateur", "En ce moment, Nino pousse la porte."),
        ("narrateur", "Nino parle peu."),
        ("narrateur", "Il regarde le carrelage, tout calme."),
        ("narrateur", "Raphaël a envie de demander plein de choses."),
        ("narrateur", "Il respire, tout doux."),
        ("maman", "On peut attendre."),
        ("maman", "On peut tendre un jouet."),
        ("papa", "On ne force pas la parole."),
        ("papa", "On n'imite pas."),
        ("papa", "On peut jouer ensemble."),
        ("narrateur", "Nino pose son sac, sans un mot."),
        ("enfant-m", "J'attends."),
        ("maman", "Tu attends, c'est bien."),
        ("narrateur", "Une goutte glisse encore sur le zinc."),
    ]

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Trois jeux attendent sur le bas de l'armoire."),
        ("papa", "Les cubes, le livre, ou la dînette ?"),
        ("maman", "On peut tendre un jouet."),
        ("maman", "On peut attendre."),
    ]

    for p1, jeu in jeux.items():
        by[f"CHK_T0001_{p1}"] = jeu_l1[jeu]
        by[f"CHK_T0001_{p1}_Q0001"] = q[jeu]
        by[f"CHK_T0001_{p1}_C0001"] = conf[jeu]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = [
            ("narrateur", "Trois goûters attendent, tout proches."),
            ("maman", "Une pomme, un yaourt, ou un morceau de pain ?"),
            ("papa", "On tend. On attend."),
        ]

        for p2, alim in aliments.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                alim_scene[alim]
                + sent(extra_jeu_alim[(jeu, alim)])
                + [
                    ("narrateur", f"On a encore {jeu_np[jeu]}, sur la table."),
                    ("maman", "On peut attendre."),
                    ("papa", "On peut jouer ensemble."),
                ]
            )
            by[f"{cid_l2}_T0003_P0000"] = [
                ("narrateur", "Un animal de la maison attend, tout près."),
                ("papa", "Le chat, le chien, ou la poule ?"),
                ("maman", "On tend un jouet. On attend."),
            ]
            sons[f"{cid_l2}_T0003_P0000"] = "chien_bonjour"

            for p3, anim in animaux.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(jeu, alim, anim)
                by[f"{cid_l3}_F0001"] = fin(jeu, alim, anim)
                if anim == "chien":
                    sons[cid_l3] = "chien_bonjour"

    write_story(
        "TREE-DIF-004",
        {
            "fil_rouge": (
                "La gouttière chante sur le zinc. Nino arrive, tout calme, "
                "et parle peu. Raphaël attend, tend un cube, une tasse, une pomme. "
                "Ils jouent ensemble, avec peu de mots."
            ),
            "title": "La gouttière et le cube de Nino",
            "characters": "Raphaël, Nino, papa, maman",
            "setting": "cuisine un jour de pluie, puis la maison",
            "secondary_lessons": "DIF.BES.002",
        },
        by,
        sons,
        max_words=16,
        extra_forbid=("Victorino", "Aniss", "Amir", "Chouchou"),
    )


def story_005() -> None:
    moments = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}
    lieux = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    objets = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    moment_np = {
        "matin": "le matin",
        "sieste": "après la sieste",
        "soir": "le soir",
    }
    lieu_np = {"cuisine": "la cuisine", "jardin": "le jardin", "chambre": "la chambre"}
    objet_np = {
        "ballon": "le ballon rouge",
        "seau": "le seau bleu",
        "doudou": "le doudou",
    }
    objet_pres = {
        "ballon": "près du ballon rouge",
        "seau": "près du seau bleu",
        "doudou": "près du doudou",
    }

    moment_l1 = {
        "matin": [
            ("narrateur", "La rosée brille encore sur le banc."),
            ("narrateur", "Le toboggan a un grain de sable."),
            ("narrateur", "Ça sent l'herbe, tout frais."),
            ("papa", "Le parc se réveille, Victorino."),
            ("enfant-m", "Oui, papa."),
            ("narrateur", "Aniss s'approche du bac."),
            ("copain", "Je veux le..."),
            ("narrateur", "Aniss cherche le mot."),
            ("narrateur", "Victorino ouvre la bouche."),
            ("papa", "On laisse le temps."),
            ("papa", "On attend la fin de la phrase."),
            ("narrateur", "Victorino referme la bouche."),
            ("narrateur", "Il pose les mains sur le banc."),
            ("copain", "Je veux le bac."),
            ("maman", "Bravo, Victorino."),
            ("maman", "Tu as su attendre."),
            ("papa", "On peut jouer ensemble."),
            ("narrateur", "Le bac à sable est encore frais."),
        ],
        "sieste": [
            ("narrateur", "Les joues d'Aniss sont encore chaudes."),
            ("narrateur", "Une mèche colle à son front."),
            ("narrateur", "Le parc est plus calme, tout doux."),
            ("maman", "La sieste est finie ?"),
            ("enfant-m", "Oui, maman."),
            ("copain", "Le bac est..."),
            ("narrateur", "Aniss s'arrête."),
            ("narrateur", "Victorino attend."),
            ("papa", "On laisse le temps."),
            ("maman", "On attend la fin de la phrase."),
            ("narrateur", "Un oiseau saute près du seau."),
            ("copain", "Le bac est chaud."),
            ("papa", "Bravo."),
            ("papa", "Tu as laissé le temps."),
            ("maman", "On peut jouer ensemble."),
            ("narrateur", "Le sable coule entre les doigts."),
        ],
        "soir": [
            ("narrateur", "Le parc devient bleu, tout doux."),
            ("narrateur", "Le banc a perdu sa chaleur."),
            ("narrateur", "Un lampadaire s'allume, tout loin."),
            ("papa", "On rentre bientôt."),
            ("enfant-m", "Encore un peu."),
            ("copain", "Je rentre avec..."),
            ("narrateur", "Aniss cherche le mot."),
            ("narrateur", "Victorino attend la fin."),
            ("maman", "On laisse le temps."),
            ("maman", "On attend la fin de la phrase."),
            ("copain", "Je rentre avec vous."),
            ("papa", "Bravo, Victorino."),
            ("papa", "Tu as su attendre."),
            ("maman", "On peut jouer ensemble."),
            ("narrateur", "Le seau bleu penche sur le sable."),
        ],
    }

    q = {
        "matin": [
            ("narrateur", "Aniss cherche un mot."),
            ("papa", "On laisse le temps ?"),
        ],
        "sieste": [
            ("narrateur", "Aniss n'a pas fini."),
            ("maman", "On attend la fin ?"),
        ],
        "soir": [
            ("narrateur", "Aniss parle tout doucement."),
            ("papa", "On attend la fin de la phrase ?"),
        ],
    }

    conf = {
        "matin": [
            ("maman", "Oui."),
            ("maman", "On laisse le temps."),
            ("papa", "On attend la fin de la phrase."),
            ("narrateur", "Victorino souffle un peu."),
            ("enfant-m", "J'attends."),
            ("papa", "Bravo, Victorino."),
            ("papa", "C'est du bon travail."),
            ("narrateur", "Le banc reste tiède sous les mains."),
        ],
        "sieste": [
            ("papa", "Oui."),
            ("papa", "On laisse le temps."),
            ("maman", "On attend la fin de la phrase."),
            ("narrateur", "Victorino garde les lèvres fermées."),
            ("enfant-m", "J'ai attendu."),
            ("maman", "Bravo."),
            ("maman", "Tu as laissé le temps."),
            ("narrateur", "Une feuille tourne dans la flaque."),
        ],
        "soir": [
            ("maman", "Oui."),
            ("maman", "On laisse le temps."),
            ("papa", "On attend la fin de la phrase."),
            ("narrateur", "Victorino hoche la tête."),
            ("enfant-m", "Jusqu'au bout."),
            ("papa", "Bravo."),
            ("papa", "On peut jouer ensemble."),
            ("narrateur", "Le lampadaire fait un rond jaune."),
        ],
    }

    lieu_l2 = {
        "cuisine": [
            ("narrateur", "Plus tard, la cuisine sent le pain."),
            ("narrateur", "La nappe est un peu rêche."),
            ("narrateur", "Une miette dort près du sel."),
            ("maman", "On se lave les mains ?"),
            ("enfant-m", "Oui, maman."),
            ("copain", "Le pain est..."),
            ("narrateur", "Aniss s'arrête."),
            ("narrateur", "Victorino attend."),
            ("papa", "On laisse le temps."),
            ("papa", "On attend la fin de la phrase."),
            ("copain", "Le pain est tiède."),
            ("maman", "Bravo, Victorino."),
            ("maman", "Tu as su attendre."),
            ("narrateur", "L'eau coule, tout petit bruit."),
        ],
        "jardin": [
            ("narrateur", "Plus tard, le jardin a de l'herbe mouillée."),
            ("narrateur", "Une feuille colle à la chaussette."),
            ("narrateur", "Le banc de bois reste froid."),
            ("papa", "Tu sens l'herbe ?"),
            ("enfant-m", "Elle sent vert."),
            ("copain", "Le ballon a..."),
            ("narrateur", "Aniss cherche."),
            ("narrateur", "Victorino attend la fin."),
            ("maman", "On laisse le temps."),
            ("maman", "On attend la fin de la phrase."),
            ("copain", "Le ballon a de l'herbe."),
            ("papa", "Bravo."),
            ("papa", "Tu as laissé le temps."),
            ("narrateur", "Une goutte glisse sur le ballon."),
        ],
        "chambre": [
            ("narrateur", "Plus tard, la chambre est un peu sombre."),
            ("narrateur", "Le parquet craque, tout petit."),
            ("narrateur", "Le doudou attend sur l'oreiller."),
            ("maman", "On range les chaussons ?"),
            ("enfant-m", "Oui."),
            ("copain", "Le doudou va..."),
            ("narrateur", "Aniss s'arrête."),
            ("narrateur", "Victorino pose les mains à plat."),
            ("papa", "On laisse le temps."),
            ("papa", "On attend la fin de la phrase."),
            ("copain", "Le doudou va au lit."),
            ("maman", "Bravo, Victorino."),
            ("maman", "C'est du bon travail."),
            ("narrateur", "Un rayon pose sur le plaid."),
        ],
    }

    extra_moment_lieu = {
        ("matin", "cuisine"): "Un rayon jaune touche le saladier.",
        ("matin", "jardin"): "La rosée brille encore sur l'herbe.",
        ("matin", "chambre"): "Le plaid est encore frais, tout doux.",
        ("sieste", "cuisine"): "Le bol de cacao est encore tiède.",
        ("sieste", "jardin"): "L'ombre de l'arbre est ronde, tout calme.",
        ("sieste", "chambre"): "L'oreiller a encore un pli chaud.",
        ("soir", "cuisine"): "La lampe allonge l'ombre du pain.",
        ("soir", "jardin"): "Le jardin sent la terre, tout frais.",
        ("soir", "chambre"): "La veilleuse fait un rond orange.",
    }

    objet_scene = {
        "ballon": [
            ("narrateur", "Victorino prend le ballon rouge."),
            ("narrateur", "Le caoutchouc est un peu rêche."),
            ("copain", "Le ballon est..."),
            ("narrateur", "Aniss cherche."),
            ("narrateur", "Victorino attend."),
            ("papa", "On laisse le temps."),
            ("copain", "Le ballon est rouge."),
            ("maman", "Bravo."),
            ("maman", "Tu as attendu la fin."),
            ("enfant-m", "Il est rouge, oui."),
            ("papa", "On peut jouer ensemble."),
        ],
        "seau": [
            ("narrateur", "Victorino pose le seau bleu."),
            ("narrateur", "Le plastique sonne, tout creux."),
            ("copain", "Le seau est..."),
            ("narrateur", "Aniss s'arrête."),
            ("narrateur", "Victorino attend la fin."),
            ("maman", "On laisse le temps."),
            ("copain", "Le seau est bleu."),
            ("papa", "Bravo, Victorino."),
            ("papa", "Tu as su attendre."),
            ("enfant-m", "Il est bleu."),
            ("maman", "On peut jouer ensemble."),
        ],
        "doudou": [
            ("narrateur", "Victorino prend le doudou."),
            ("narrateur", "Le tissu est doux, un peu lourd."),
            ("copain", "Le doudou va..."),
            ("narrateur", "Aniss cherche le mot."),
            ("narrateur", "Victorino attend."),
            ("papa", "On attend la fin de la phrase."),
            ("copain", "Le doudou va venir."),
            ("maman", "Bravo."),
            ("maman", "Tu as laissé le temps."),
            ("enfant-m", "Il vient."),
            ("papa", "On peut jouer ensemble."),
        ],
    }

    extras_l3 = {
        ("matin", "cuisine", "ballon"): "Le ballon roule près du saladier froid.",
        ("matin", "cuisine", "seau"): "Le seau bleu sonne près de l'évier.",
        ("matin", "cuisine", "doudou"): "Le doudou sent encore le pain chaud.",
        ("matin", "jardin", "ballon"): "Le ballon a un grain d'herbe collé.",
        ("matin", "jardin", "seau"): "Le seau ramasse une feuille mouillée.",
        ("matin", "jardin", "doudou"): "Le doudou a un brin d'herbe, tout vert.",
        ("matin", "chambre", "ballon"): "Le ballon tapote le parquet, tout doux.",
        ("matin", "chambre", "seau"): "Le seau bleu est près des chaussons.",
        ("matin", "chambre", "doudou"): "Le doudou retrouve l'oreiller frais.",
        ("sieste", "cuisine", "ballon"): "Le ballon s'immobilise près du bol.",
        ("sieste", "cuisine", "seau"): "Le seau fait un bruit, tout petit.",
        ("sieste", "cuisine", "doudou"): "Le doudou est tiède, comme les joues.",
        ("sieste", "jardin", "ballon"): "Le ballon sèche au soleil, tout lent.",
        ("sieste", "jardin", "seau"): "Le seau a une ombre ronde, tout calme.",
        ("sieste", "jardin", "doudou"): "Le doudou s'assoit sur le banc froid.",
        ("sieste", "chambre", "ballon"): "Le ballon reste au pied du lit.",
        ("sieste", "chambre", "seau"): "Le seau bleu veille près du plaid.",
        ("sieste", "chambre", "doudou"): "Le doudou glisse sous la couverture.",
        ("soir", "cuisine", "ballon"): "L'ombre du ballon danse sur la nappe.",
        ("soir", "cuisine", "seau"): "Le seau reflète la lampe, tout rond.",
        ("soir", "cuisine", "doudou"): "Le doudou a une miette sur l'oreille.",
        ("soir", "jardin", "ballon"): "Le ballon roule vers la haie sombre.",
        ("soir", "jardin", "seau"): "Le seau bleu penche près du portail.",
        ("soir", "jardin", "doudou"): "Le doudou sent la terre, un peu.",
        ("soir", "chambre", "ballon"): "Le ballon dort sous la veilleuse.",
        ("soir", "chambre", "seau"): "Le seau bleu est rangé, tout sage.",
        ("soir", "chambre", "doudou"): "Le doudou retrouve l'oreiller, tout chaud.",
    }

    fin_image = {
        "matin": "Un oiseau picore encore, tout loin.",
        "sieste": "La couverture redescend, tout calme.",
        "soir": "La veilleuse reste allumée, tout doux.",
    }

    def l3(moment: str, lieu: str, objet: str) -> list[tuple[str, str]]:
        return (
            objet_scene[objet]
            + sent(extras_l3[(moment, lieu, objet)])
            + [
                ("narrateur", f"On est encore dans {lieu_np[lieu]}."),
                ("narrateur", f"C'est encore {moment_np[moment]}."),
                ("papa", "On laisse le temps."),
                ("maman", "On attend la fin de la phrase."),
                ("enfant-m", "J'ai attendu."),
                ("papa", "Bravo, Victorino."),
            ]
        )

    def fin(moment: str, lieu: str, objet: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "Merci, maman."),
            ("enfant-m", "Merci, papa."),
            ("maman", "Bravo, Victorino."),
            ("papa", "Tu as fait du bon travail."),
            ("papa", "Tu as laissé le temps."),
            ("narrateur", f"Victorino a vécu {moment_np[moment]}."),
            ("narrateur", f"Il a joué dans {lieu_np[lieu]}."),
            ("narrateur", f"Aniss a fini sa phrase, {objet_pres[objet]}."),
            ("narrateur", fin_image[moment]),
            ("narrateur", "L'histoire est finie."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le toboggan a encore du sable."),
        ("narrateur", "Un grain brille, tout chaud."),
        ("narrateur", "Une feuille tourne dans une flaque."),
        ("narrateur", "Le banc du parc est tiède."),
        ("narrateur", "Ça sent l'herbe coupée."),
        ("narrateur", "Un oiseau saute près du seau."),
        ("narrateur", "Papa noue un lacet, tout doux."),
        ("narrateur", "Maman pose le panier sur le banc."),
        ("papa", "Tu sens l'herbe, Victorino ?"),
        ("enfant-m", "Elle sent vert, papa."),
        ("maman", "Le banc est encore chaud."),
        ("narrateur", "En ce moment, Aniss arrive."),
        ("narrateur", "Il parle tout doucement."),
        ("narrateur", "Il cherche déjà un mot."),
        ("copain", "Je veux le..."),
        ("narrateur", "Aniss s'arrête."),
        ("narrateur", "Victorino ouvre la bouche."),
        ("papa", "On laisse le temps."),
        ("papa", "On attend la fin de la phrase."),
        ("narrateur", "Victorino referme la bouche."),
        ("narrateur", "Il pose les mains sur le banc."),
        ("copain", "Je veux le seau."),
        ("maman", "Bravo, Victorino."),
        ("maman", "Tu as su attendre."),
        ("papa", "On peut jouer ensemble."),
        ("narrateur", "Le seau bleu reste sur le sable."),
    ]
    sons["CHK_T0000_P0000"] = "enfants_parc"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Quel moment, maintenant ?"),
        ("papa", "Le matin, après la sieste, ou le soir ?"),
        ("maman", "On laisse le temps."),
    ]

    for p1, moment in moments.items():
        by[f"CHK_T0001_{p1}"] = moment_l1[moment]
        sons[f"CHK_T0001_{p1}"] = "enfants_parc"
        by[f"CHK_T0001_{p1}_Q0001"] = q[moment]
        by[f"CHK_T0001_{p1}_C0001"] = conf[moment]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = [
            ("narrateur", "Trois coins de la maison attendent."),
            ("maman", "La cuisine, le jardin, ou la chambre ?"),
            ("papa", "On attend la fin de la phrase."),
        ]

        for p2, lieu in lieux.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            by[cid_l2] = (
                lieu_l2[lieu]
                + sent(extra_moment_lieu[(moment, lieu)])
                + [
                    ("maman", "On laisse le temps."),
                    ("papa", "On peut jouer ensemble."),
                ]
            )
            by[f"{cid_l2}_T0003_P0000"] = [
                ("narrateur", "Trois objets attendent, tout proches."),
                ("papa", "Le ballon rouge, le seau bleu, ou le doudou ?"),
                ("maman", "On laisse le temps."),
            ]

            for p3, objet in objets.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(moment, lieu, objet)
                by[f"{cid_l3}_F0001"] = fin(moment, lieu, objet)

    write_story(
        "TREE-DIF-005",
        {
            "fil_rouge": (
                "Le sable colle au toboggan. Aniss cherche ses mots. "
                "Victorino attend la fin de la phrase. Le ballon, le seau, "
                "le doudou. Les phrases se finissent, tout doucement."
            ),
            "title": "Le sable du toboggan et la phrase d'Aniss",
            "characters": "Victorino, Aniss, papa, maman",
            "setting": "parc, puis la maison",
            "secondary_lessons": "DIF.PAR.001",
        },
        by,
        sons,
        max_words=12,
        extra_forbid=("Raphaël", "Nino", "Sarah", "Mila"),
    )


if __name__ == "__main__":
    story_004()
    story_005()
    print("ok TREE-DIF-004 TREE-DIF-005")
