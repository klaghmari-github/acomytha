#!/usr/bin/env python3
"""Passe orale TREE-AUT-001 : plus de puces (première/deuxième, faits empilés)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from _lib import check, from_script

MERGED = ROOT / "TREE-AUT-001" / "merged.json"


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    return from_script([f"{r}|{p}" for r, p in lines])


opening = pack([
    ("narrateur", "Au bout de la rue, une petite maison."),
    ("narrateur", "Amir vit là, avec papa et maman."),
    ("narrateur", "Le jardin derrière est minuscule, encore mouillé."),
    ("narrateur", "Ce matin-là, la pluie vient de partir."),
    ("narrateur", "Les pavés brillent derrière la fenêtre."),
    ("narrateur", "Dans la cuisine, ça sent déjà la soupe."),
    ("narrateur", "Papa travaille près du volet jaune."),
    ("narrateur", "Son ordinateur souffle, tout doux."),
    ("narrateur", "En ce moment, Amir plie une feuille."),
    ("narrateur", "Les plis font une coque, puis une voile."),
    ("enfant-m", "Capitaine Amir est prêt !"),
    ("narrateur", "Il pousse le bateau vers la pantoufle de papa."),
    ("papa", "Votre navire cherche-t-il la mer ?"),
    ("enfant-m", "Oui, mais la mer est très loin."),
    ("narrateur", "Une goutte tombe dehors, puis une autre."),
    ("narrateur", "Amir colle son nez contre la vitre."),
    ("narrateur", "L'eau a dessiné des chemins dans le jardin."),
    ("enfant-m", "Papa, mon bateau peut voyager ici !"),
    ("papa", "Alors rapporte-nous une grande histoire."),
    ("enfant-m", "Et peut-être un trésor !"),
    ("papa", "Merci, on t'attendra."),
    ("narrateur", "Maman pose le petit sac près d'Amir."),
    ("maman", "Prépare-toi, avant que le soleil sèche tout."),
])

t1 = pack([
    ("narrateur", "Avant de sortir, Amir prépare ses affaires."),
    ("narrateur", "Il y a le manteau, les bottes, et le linge."),
    ("maman", "Laquelle prépares-tu d'abord ?"),
])

t2 = pack([
    ("narrateur", "Dehors, l'eau brille encore un peu."),
    ("narrateur", "Un chemin part de la gouttière."),
    ("narrateur", "Un autre se cache entre les choux."),
    ("narrateur", "Le bac a l'air d'une petite île."),
    ("papa", "Quelle route choisis-tu, capitaine ?"),
])

prep = {
    1: {
        "scene": pack([
            ("narrateur", "Amir cherche d'abord son manteau jaune."),
            ("narrateur", "Une manche est encore retournée."),
            ("enfant-m", "Je l'ai trouvée !"),
            ("narrateur", "Il la remet dans le bon sens."),
            ("maman", "Ton manteau est prêt."),
            ("narrateur", "Ensuite, le bateau glisse dans le sac."),
            ("narrateur", "Maman glisse le petit linge à côté."),
            ("narrateur", "Les bottes attendent déjà près de la porte."),
        ]),
        "question": pack([("narrateur", "Où Amir range-t-il son bateau ?")]),
        "answer": ("dans le sac", "sac|le sac|dans le sac|au fond du sac", "Le bateau est dans le sac."),
        "confirm": pack([
            ("narrateur", "Le bateau repose au fond du sac, sous le linge."),
            ("papa", "Bottes aux pieds, capitaine ?"),
            ("enfant-m", "Bottes aux pieds, manteau fermé !"),
        ]),
        "arrival": {
            1: "Le manteau jaune brille encore sous la gouttière.",
            2: "Une odeur de soupe reste dans son col.",
            3: "Le vent gonfle doucement son manteau jaune.",
        },
        "coda": [
            ("narrateur", "À la porte, Amir suspend son manteau."),
            ("narrateur", "Une goutte glisse encore de la capuche."),
        ],
    },
    2: {
        "scene": pack([
            ("narrateur", "Amir choisit d'abord ses bottes rouges."),
            ("narrateur", "Une botte porte encore un peu de boue."),
            ("maman", "Je te montre un petit coin."),
            ("narrateur", "Maman passe le linge, puis Amir frotte."),
            ("enfant-m", "Elle est prête !"),
            ("narrateur", "Le bateau rejoint le sac."),
            ("narrateur", "Le manteau attend encore sur la chaise."),
        ]),
        "question": pack([("narrateur", "Qui termine d'essuyer la botte ?")]),
        "answer": ("Amir", "amir|c'est amir|amir termine|le garçon", "Amir termine d'essuyer la botte."),
        "confirm": pack([
            ("narrateur", "La semelle rouge est propre, enfin."),
            ("narrateur", "Amir enfile les deux bottes."),
            ("papa", "Et le manteau, capitaine ?"),
            ("enfant-m", "Fermé jusqu'en haut !"),
        ]),
        "arrival": {
            1: "Ses bottes font floc sous la gouttière.",
            2: "Ses bottes traversent la terre molle.",
            3: "Ses bottes s'arrêtent au bord du sable.",
        },
        "coda": [
            ("narrateur", "À la porte, Amir retire ses bottes."),
            ("narrateur", "Deux traces rouges restent sur le tapis."),
        ],
    },
    3: {
        "scene": pack([
            ("narrateur", "Amir prend d'abord le petit linge bleu."),
            ("narrateur", "Il est encore chaud du radiateur."),
            ("maman", "À quoi servira-t-il ?"),
            ("enfant-m", "À sauver mon bateau mouillé."),
            ("narrateur", "Il le roule comme un petit coussin."),
            ("narrateur", "Le bateau se pose dessus, dans le sac."),
            ("narrateur", "Le manteau et les bottes sont déjà prêts."),
        ]),
        "question": pack([("narrateur", "Où Amir met-il le petit linge ?")]),
        "answer": ("dans le sac", "sac|le sac|dans le sac", "Le petit linge va dans le sac."),
        "confirm": pack([
            ("narrateur", "Le linge protège le bateau."),
            ("narrateur", "Amir ferme doucement le sac."),
            ("papa", "Tout est prêt, capitaine ?"),
            ("enfant-m", "Manteau, bottes et bateau !"),
        ]),
        "arrival": {
            1: "Le linge bleu attend dans le sac.",
            2: "Le linge garde encore un peu de chaleur.",
            3: "Le linge attend le bateau mouillé.",
        },
        "coda": [
            ("narrateur", "Amir enveloppe le bateau dans le linge."),
            ("narrateur", "Une tache humide dessine une petite île."),
        ],
    },
}

routes = {
    1: {
        "labels": ["attendre trois gouttes", "demander l'aide de papa", "chercher un autre départ"],
        "prompt": pack([
            ("narrateur", "La feuille tient bon, et l'eau baisse."),
            ("papa", "Que tente le capitaine ?"),
        ]),
        "acts": {
            1: pack([
                ("enfant-m", "J'attends trois gouttes."),
                ("narrateur", "Une goutte frappe la feuille."),
                ("narrateur", "Puis une autre soulève le bord."),
                ("narrateur", "La dernière la fait pivoter."),
                ("narrateur", "Un passage étroit apparaît."),
                ("enfant-m", "Maintenant, petit bateau !"),
                ("narrateur", "Le bateau file sous une brindille."),
            ]),
            2: pack([
                ("enfant-m", "Papa, j'ai besoin de toi."),
                ("papa", "Tiens le bateau contre le courant."),
                ("narrateur", "Papa soulève doucement la feuille."),
                ("narrateur", "Amir maintient la coque bien droite."),
                ("papa", "Maintenant, laisse-le partir."),
                ("narrateur", "Le bateau bondit dans l'eau libre."),
            ]),
            3: pack([
                ("enfant-m", "Je cherche un autre départ."),
                ("narrateur", "Amir longe la rivière sans courir."),
                ("narrateur", "Derrière un pot, l'eau recommence."),
                ("narrateur", "Il pose le bateau après la feuille."),
                ("narrateur", "Le courant l'emporte vers les violettes."),
                ("enfant-m", "J'ai trouvé le passage secret !"),
            ]),
        },
        "endings": {
            1: pack([
                ("narrateur", "Le bateau atteint le pot violet."),
                ("narrateur", "Une petite feuille colle devant."),
                ("narrateur", "Amir la garde comme drapeau."),
                ("narrateur", "Puis il rentre avant la dernière goutte."),
                ("papa", "Quel trésor rapporte votre navire ?"),
                ("enfant-m", "Un drapeau gagné après trois gouttes."),
            ]),
            2: pack([
                ("narrateur", "Le bateau traverse la rivière délivrée."),
                ("narrateur", "Une ligne brillante marque sa coque."),
                ("narrateur", "Amir la montre en rentrant."),
                ("papa", "Nous avons formé un bon équipage."),
                ("enfant-m", "Moi devant, et toi derrière !"),
            ]),
            3: pack([
                ("narrateur", "Le courant dépose une brindille sur la voile."),
                ("narrateur", "Amir rapporte le bateau ainsi décoré."),
                ("papa", "Je reconnais le passage secret."),
                ("enfant-m", "Il commence derrière le grand pot."),
            ]),
        },
    },
    2: {
        "labels": ["compter les passages", "attendre le courant", "demander conseil à maman"],
        "prompt": pack([
            ("narrateur", "Le port semble fermé."),
            ("narrateur", "Derrière, la terre forme un petit quai."),
            ("maman", "Comment entrera ton bateau ?"),
        ]),
        "acts": {
            1: pack([
                ("narrateur", "Amir observe les trois feuilles."),
                ("enfant-m", "Une, deux, trois."),
                ("narrateur", "Entre deux et trois, l'eau brille."),
                ("narrateur", "Il guide doucement le bateau."),
                ("narrateur", "Le bateau traverse sans toucher les choux."),
                ("enfant-m", "Quai numéro deux !"),
            ]),
            2: pack([
                ("enfant-m", "J'attends le prochain courant."),
                ("narrateur", "Amir garde le bateau contre sa botte."),
                ("narrateur", "L'eau pousse lentement une feuille."),
                ("narrateur", "Puis une autre s'écarte aussi."),
                ("narrateur", "Le port s'ouvre juste assez."),
                ("narrateur", "Le bateau glisse jusqu'au quai."),
            ]),
            3: pack([
                ("enfant-m", "Maman, peux-tu regarder mon port ?"),
                ("maman", "Vois-tu cette rigole près du thym ?"),
                ("narrateur", "Amir suit la rigole avec son doigt."),
                ("narrateur", "Elle contourne toutes les jeunes pousses."),
                ("enfant-m", "Voilà ma route !"),
                ("narrateur", "Le bateau rejoint le quai sans rien plier."),
            ]),
        },
        "endings": {
            1: pack([
                ("narrateur", "Au quai, une feuille devient drapeau."),
                ("narrateur", "Amir la plante dans le sable humide."),
                ("narrateur", "Les trois choux restent bien droits."),
                ("narrateur", "À table, Amir dessine son port."),
                ("maman", "Quel passage as-tu choisi ?"),
                ("enfant-m", "Celui entre deux et trois."),
            ]),
            2: pack([
                ("narrateur", "Le bateau touche enfin le quai de terre."),
                ("narrateur", "Une odeur de chou monte de sa coque."),
                ("narrateur", "Amir éclate de rire en rentrant."),
                ("papa", "Ton trésor sent vraiment le potager !"),
                ("enfant-m", "C'est le parfum de mon port."),
            ]),
            3: pack([
                ("narrateur", "La rigole conduit le bateau au thym."),
                ("narrateur", "Une minuscule fleur touche sa voile."),
                ("narrateur", "Amir rentre avec son bateau parfumé."),
                ("maman", "Tu as trouvé sans écraser mes choux."),
                ("enfant-m", "La route passait près du thym."),
            ]),
        },
    },
    3: {
        "labels": ["chercher une autre flaque", "creuser un petit canal", "faire une piste de sable"],
        "prompt": pack([
            ("narrateur", "Le bateau attend dans les mains d'Amir."),
            ("narrateur", "Le caillou blanc reste hors d'atteinte."),
            ("papa", "Comment sauver ce voyage ?"),
        ]),
        "acts": {
            1: pack([
                ("enfant-m", "Je cherche une autre flaque."),
                ("narrateur", "Amir regarde autour du bac."),
                ("narrateur", "Sous le banc, une eau claire résiste."),
                ("narrateur", "Il y pose vite son bateau."),
                ("narrateur", "Le bateau contourne un galet gris."),
                ("enfant-m", "Une nouvelle île !"),
            ]),
            2: pack([
                ("enfant-m", "Je creuse un petit canal."),
                ("narrateur", "Amir prend la pelle du bac."),
                ("narrateur", "Papa verse doucement un fond d'arrosoir."),
                ("narrateur", "L'eau suit le canal jusqu'au caillou."),
                ("narrateur", "Le bateau avance dans cette rivière neuve."),
                ("enfant-m", "L'île revient !"),
            ]),
            3: pack([
                ("enfant-m", "Je fabrique une piste de sable."),
                ("narrateur", "Amir tasse une longue bande humide."),
                ("narrateur", "Il pose la coque bien droite."),
                ("narrateur", "Puis il souffle dans la voile."),
                ("narrateur", "Le bateau glisse jusqu'au caillou blanc."),
                ("enfant-m", "Mon bateau roule aussi !"),
            ]),
        },
        "endings": {
            1: pack([
                ("narrateur", "Le galet gris devient le nouveau trésor."),
                ("narrateur", "Amir le laisse près de la flaque."),
                ("narrateur", "Il rapporte seulement son histoire."),
                ("papa", "L'île a changé, mais le voyage continue."),
                ("enfant-m", "Demain, je chercherai encore."),
            ]),
            2: pack([
                ("narrateur", "Le bateau atteint enfin le caillou blanc."),
                ("narrateur", "Son reflet danse dans le petit canal."),
                ("narrateur", "Puis l'eau disparaît doucement dans le sable."),
                ("enfant-m", "J'ai vu mon île revenir."),
                ("papa", "Juste assez longtemps pour ton voyage."),
            ]),
            3: pack([
                ("narrateur", "Le devant touche doucement le caillou blanc."),
                ("narrateur", "Un grain doré reste sur la coque."),
                ("narrateur", "Amir le montre à papa en rentrant."),
                ("papa", "Un vrai trésor de capitaine."),
                ("enfant-m", "Mon bateau connaît aussi les routes."),
            ]),
        },
    },
}


def arrival(p: int, route: int) -> tuple[str, str]:
    flavor = prep[p]["arrival"][route]
    if route == 1:
        return pack([
            ("narrateur", flavor),
            ("narrateur", "Une rigole court encore sous la gouttière."),
            ("narrateur", "Amir pose le bateau sur l'eau, tout doux."),
            ("narrateur", "Le voyage commence, enfin."),
            ("narrateur", "Soudain, une grande feuille tourne et bouche tout."),
            ("narrateur", "Le bateau s'arrête juste derrière."),
            ("enfant-m", "Vite, le soleil revient !"),
            ("papa", "L'eau baisse déjà."),
        ])
    if route == 2:
        return pack([
            ("narrateur", flavor),
            ("narrateur", "Entre les choux se cache un petit port."),
            ("narrateur", "Trois feuilles flottent devant l'entrée."),
            ("narrateur", "Le bateau avance, tout doucement."),
            ("narrateur", "L'une touche sa voile."),
            ("narrateur", "Une autre ferme le passage."),
            ("narrateur", "La dernière frôle un jeune chou."),
            ("enfant-m", "Je ne veux rien abîmer."),
            ("narrateur", "Amir retient aussitôt son bateau."),
        ])
    return pack([
        ("narrateur", flavor),
        ("narrateur", "Devant le bac brille une île ronde."),
        ("narrateur", "Au milieu repose un caillou blanc."),
        ("enfant-m", "Voilà l'île au trésor !"),
        ("narrateur", "Amir approche le bateau de l'eau."),
        ("narrateur", "Mais la flaque devient soudain plus petite."),
        ("narrateur", "Le sable boit ses derniers reflets."),
        ("enfant-m", "Mon île disparaît !"),
        ("papa", "Il reste encore un peu de temps."),
    ])


def ending(p: int, route: int, res: int) -> tuple[str, str]:
    body = routes[route]["endings"][res][1].splitlines()
    extra = [
        f"{r}|{ph}" for r, ph in prep[p]["coda"]
    ] + [
        "narrateur|Le bateau sèche près du volet.",
        "maman|La soupe est prête.",
    ]
    return from_script(body + extra)


def put(store: dict, cid: str, packed: tuple[str, str]) -> None:
    store[cid] = packed


def main() -> None:
    texts: dict[str, tuple[str, str]] = {}
    questions: dict[str, tuple[str, str, str]] = {}
    labels: dict[str, list[str]] = {}

    put(texts, "CHK_T0000_P0000", opening)
    put(texts, "CHK_T0001_P0000", t1)
    labels["CHK_T0001_P0000"] = ["le manteau", "les bottes", "le petit linge"]

    for p in (1, 2, 3):
        base = f"CHK_T0001_P000{p}"
        put(texts, base, prep[p]["scene"])
        put(texts, f"{base}_Q0001", prep[p]["question"])
        questions[f"{base}_Q0001"] = prep[p]["answer"]
        put(texts, f"{base}_C0001", prep[p]["confirm"])
        put(texts, f"{base}_T0002_P0000", t2)
        labels[f"{base}_T0002_P0000"] = [
            "la rivière de la gouttière",
            "le port des choux",
            "l'île du bac",
        ]
        for route in (1, 2, 3):
            rb = f"{base}_T0002_P000{route}"
            put(texts, rb, arrival(p, route))
            put(texts, f"{rb}_T0003_P0000", routes[route]["prompt"])
            labels[f"{rb}_T0003_P0000"] = routes[route]["labels"]
            for res in (1, 2, 3):
                eb = f"{rb}_T0003_P000{res}"
                put(texts, eb, routes[route]["acts"][res])
                put(texts, f"{eb}_F0001", ending(p, route, res))

    data = json.loads(MERGED.read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in data["chunks"] if c["chunk_id"] not in texts]
    extra = set(texts) - {c["chunk_id"] for c in data["chunks"]}
    if missing or extra:
        raise SystemExit(f"ids missing={missing} extra={extra}")

    for chunk in data["chunks"]:
        cid = chunk["chunk_id"]
        text, script = texts[cid]
        chunk["text"] = text
        chunk["script"] = script
        chunk["text_ssml"] = text
        chunk["text_xai_tags"] = text
        if cid in labels:
            a, b, c = labels[cid]
            chunk["option_1_label"] = a
            chunk["option_2_label"] = b
            chunk["option_3_label"] = c
        if cid in questions:
            exp, acc, retry = questions[cid]
            chunk["expected_answer"] = exp
            chunk["accepted_examples"] = acc
            chunk["retry_prompt"] = retry

    check("TREE-AUT-001", data.get("age_band") or "N1", data["chunks"])
    MERGED.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MERGED}  {len(texts)} chunks")


if __name__ == "__main__":
    main()
