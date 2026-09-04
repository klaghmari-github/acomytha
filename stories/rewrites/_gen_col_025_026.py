#!/usr/bin/env python3
"""Génère merged.json pour TREE-COL-025 et TREE-COL-026 (texte seulement)."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent


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


def write_story(story_id: str, meta: dict, by_id: dict[str, list[tuple[str, str]]], sons_map: dict[str, str]) -> None:
    folder = ROOT / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_id]
    extra = [k for k in by_id if k not in {c["chunk_id"] for c in source["chunks"]}]
    if missing or extra:
        raise SystemExit(f"{story_id} missing={missing[:12]} extra={extra[:12]}")
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


def story_025() -> None:
    places = {"P0001": "cuisine", "P0002": "jardin", "P0003": "chambre"}
    toys = {"P0001": "cubes", "P0002": "livre", "P0003": "dinette"}
    times = {"P0001": "matin", "P0002": "sieste", "P0003": "soir"}

    place_l1 = {
        "cuisine": [
            ("narrateur", "Nina pousse la porte de la cuisine."),
            ("narrateur", "La poignée est un peu tiède."),
            ("narrateur", "La soupe fume encore, tout doux."),
            ("narrateur", "Des miettes dorées restent sur la table."),
            ("narrateur", "La cuillère en bois brille, un peu humide."),
            ("papa", "Viens près de la table, Nina."),
            ("papa", "Moi, je raconte la soupe."),
            ("narrateur", "Papa parle jusqu'au bout."),
            ("narrateur", "Nina a une chose à dire."),
            ("narrateur", "Elle lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "C'est mon tour ?"),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina parle, tout doucement."),
            ("enfant-f", "La soupe sent la carotte."),
            ("maman", "Bravo, Nina."),
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", "Une goutte tombe encore, dans l'évier."),
            ("papa", "On peut lever la main, encore."),
        ],
        "jardin": [
            ("narrateur", "Nina ouvre la porte du jardin."),
            ("narrateur", "L'air est frais, un peu mouillé."),
            ("narrateur", "L'herbe brille, toute verte."),
            ("narrateur", "Une feuille collée au sabot fait un petit bruit."),
            ("narrateur", "Un oiseau picore sous le cerisier, tout loin."),
            ("maman", "Viens sous l'auvent, Nina."),
            ("maman", "Moi, je raconte l'oiseau."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "L'herbe est toute brillante."),
            ("papa", "Oui."),
            ("papa", "Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina pose un pied dans l'herbe, tout doux."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", "Une goutte tombe d'une feuille, tout loin."),
            ("papa", "On peut lever la main, dans le jardin aussi."),
        ],
        "chambre": [
            ("narrateur", "Nina entre dans la chambre."),
            ("narrateur", "Le tapis est chaud sous les pieds."),
            ("narrateur", "Le doudou attend au bord du lit."),
            ("narrateur", "Un rayon glisse sur l'oreiller, tout pâle."),
            ("narrateur", "Le rideau bouge, tout léger."),
            ("papa", "Assieds-toi, Nina."),
            ("papa", "Moi, je raconte le doudou."),
            ("narrateur", "Papa parle, tout calme."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("enfant-f", "L'oreiller est tout doux."),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "On a attendu."),
            ("maman", "Puis on parle."),
            ("narrateur", "Nina caresse le doudou, tout bas."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as attendu."),
            ("papa", "Puis tu as parlé."),
            ("narrateur", "Le rideau fait une ombre ronde."),
            ("maman", "On peut lever la main, ici aussi."),
        ],
    }

    q = {
        "cuisine": [
            ("narrateur", "Nina veut parler, dans la cuisine."),
            ("papa", "Elle fait quoi d'abord ?"),
        ],
        "jardin": [
            ("narrateur", "Nina veut parler, dans le jardin."),
            ("maman", "Elle fait quoi d'abord ?"),
        ],
        "chambre": [
            ("narrateur", "Nina veut parler, dans la chambre."),
            ("papa", "Elle fait quoi d'abord ?"),
        ],
    }

    conf = {
        "cuisine": [
            ("papa", "Oui."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina souffle un peu."),
            ("narrateur", "Sa main redescend, tout doux."),
            ("narrateur", "La soupe fume encore, tout près."),
            ("enfant-f", "J'ai attendu."),
            ("maman", "Bravo."),
            ("maman", "Tu peux lever la main, la prochaine fois aussi."),
            ("papa", "C'est du bon travail, Nina."),
            ("narrateur", "Une miette dorée reste sur la table."),
            ("maman", "Tu as parlé, après avoir attendu."),
        ],
        "jardin": [
            ("maman", "Oui."),
            ("maman", "On lève la main."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Nina essuie une goutte sur sa manche."),
            ("narrateur", "L'herbe sent le vert, tout frais."),
            ("enfant-f", "J'ai levé la main."),
            ("papa", "Bravo, Nina."),
            ("papa", "Tu as attendu ton tour."),
            ("narrateur", "L'oiseau s'envole, tout loin."),
            ("maman", "C'est du bon travail."),
            ("maman", "On continue ensemble."),
        ],
        "chambre": [
            ("papa", "Oui."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina pose la joue sur l'oreiller."),
            ("narrateur", "Le tissu est chaud, un peu froissé."),
            ("enfant-f", "J'ai attendu."),
            ("enfant-f", "Puis j'ai parlé."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
            ("papa", "C'est du bon travail, Nina."),
            ("narrateur", "Le doudou reste au bord du lit."),
            ("maman", "On peut lever la main, encore."),
        ],
    }

    toy_scene = {
        "cubes": [
            ("narrateur", "Nina prend les cubes en bois."),
            ("narrateur", "Ils font clic, tout doux."),
            ("narrateur", "Un cube rouge a un coin un peu rêche."),
            ("papa", "Moi, je pose le premier cube."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("papa", "C'est ton tour."),
            ("enfant-f", "Le cube rouge, s'il te plaît."),
            ("maman", "Oui."),
            ("maman", "Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina pose le cube, tout droit."),
            ("maman", "Bravo."),
        ],
        "livre": [
            ("narrateur", "Nina ouvre le livre."),
            ("narrateur", "La couverture est douce, un peu froide."),
            ("narrateur", "Une image montre un bateau jaune."),
            ("maman", "Moi, je raconte le bateau."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("maman", "C'est ton tour, Nina."),
            ("enfant-f", "Le bateau est jaune."),
            ("papa", "Oui."),
            ("papa", "Merci d'avoir attendu."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Nina tourne une page, tout lentement."),
            ("papa", "Bravo."),
        ],
        "dinette": [
            ("narrateur", "Nina pose la dînette."),
            ("narrateur", "Les petites assiettes font ting."),
            ("narrateur", "Une tasse rouge est un peu de travers."),
            ("papa", "Moi, je sers l'eau, tout doux."),
            ("narrateur", "Papa parle."),
            ("narrateur", "Nina lève la main."),
            ("narrateur", "Elle attend."),
            ("papa", "C'est ton tour."),
            ("enfant-f", "La tasse, s'il te plaît."),
            ("maman", "Oui."),
            ("maman", "Tu as attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Nina tient la tasse à deux mains."),
            ("maman", "Bravo, Nina."),
        ],
    }

    extra_toy = {
        ("cuisine", "cubes"): "Un cube sent encore la soupe, tout près de la table.",
        ("cuisine", "livre"): "Le bateau jaune brille, près de la cuillère en bois.",
        ("cuisine", "dinette"): "La petite tasse fume, comme la vraie soupe.",
        ("jardin", "cubes"): "Un cube a une goutte d'herbe, tout verte.",
        ("jardin", "livre"): "Le vent tourne une page, tout léger.",
        ("jardin", "dinette"): "Une feuille tombe dans une petite assiette.",
        ("chambre", "cubes"): "Un cube rouge reste sur le tapis chaud.",
        ("chambre", "livre"): "Le bateau jaune veille près du doudou.",
        ("chambre", "dinette"): "La petite tasse est posée près de l'oreiller.",
    }

    time_open = {
        "matin": [
            ("narrateur", "Le matin, le pain est encore chaud."),
            ("narrateur", "Ça sent la croûte, toute dorée."),
            ("narrateur", "Un rayon touche la nappe."),
            ("papa", "Bonjour, Nina."),
            ("maman", "Tu as dormi ?"),
            ("enfant-f", "Un peu."),
        ],
        "sieste": [
            ("narrateur", "Après la sieste, la couverture est tiède."),
            ("narrateur", "Une joue de Nina est encore marquée."),
            ("narrateur", "Le volet fait une raie de lumière."),
            ("maman", "Tu es réveillée ?"),
            ("enfant-f", "Oui, maman."),
            ("papa", "Viens."),
            ("papa", "On a le temps."),
        ],
        "soir": [
            ("narrateur", "Le soir, la lampe fait un rond jaune."),
            ("narrateur", "Le sol est un peu froid, près de la porte."),
            ("narrateur", "Ça sent encore la soupe, tout loin."),
            ("papa", "Te voilà."),
            ("maman", "Assieds-toi, Nina."),
            ("enfant-f", "J'ai une chose."),
        ],
    }

    extras_l3 = {
        ("cuisine", "cubes", "matin"): "Le cube rouge est près de la miette dorée.",
        ("cuisine", "cubes", "sieste"): "Le cube rouge a glissé sous la couverture.",
        ("cuisine", "cubes", "soir"): "Le cube rouge brille sous la lampe.",
        ("cuisine", "livre", "matin"): "Le bateau jaune est près du pain chaud.",
        ("cuisine", "livre", "sieste"): "Le livre reste ouvert, tout calme.",
        ("cuisine", "livre", "soir"): "Le bateau jaune veille sous la lampe.",
        ("cuisine", "dinette", "matin"): "La petite tasse est près du bol de pain.",
        ("cuisine", "dinette", "sieste"): "La petite tasse chauffe au soleil du volet.",
        ("cuisine", "dinette", "soir"): "La petite tasse est loin de la vraie soupe.",
        ("jardin", "cubes", "matin"): "Le cube a encore une goutte d'herbe.",
        ("jardin", "cubes", "sieste"): "Le cube sent l'herbe, tout frais.",
        ("jardin", "cubes", "soir"): "Le cube est près de la porte du jardin.",
        ("jardin", "livre", "matin"): "Une page sent encore la pluie.",
        ("jardin", "livre", "sieste"): "Le bateau jaune a une feuille collée.",
        ("jardin", "livre", "soir"): "Le livre est près des bottes, tout calme.",
        ("jardin", "dinette", "matin"): "La petite assiette a une goutte d'herbe.",
        ("jardin", "dinette", "sieste"): "La petite tasse a séché, tout doux.",
        ("jardin", "dinette", "soir"): "La petite assiette brille sous la lampe.",
        ("chambre", "cubes", "matin"): "Le cube rouge est sur l'oreiller.",
        ("chambre", "cubes", "sieste"): "Le cube rouge dort près du doudou.",
        ("chambre", "cubes", "soir"): "Le cube rouge est au bord du lit.",
        ("chambre", "livre", "matin"): "Le bateau jaune est sous le rideau.",
        ("chambre", "livre", "sieste"): "Le livre est tiède, après la sieste.",
        ("chambre", "livre", "soir"): "Le bateau jaune veille près de la lampe.",
        ("chambre", "dinette", "matin"): "La petite tasse est près du doudou.",
        ("chambre", "dinette", "sieste"): "La petite assiette est sous la couverture.",
        ("chambre", "dinette", "soir"): "La petite tasse brille, tout bas.",
    }

    toy_np = {"cubes": "les cubes", "livre": "le livre", "dinette": "la dînette"}
    place_np = {"cuisine": "la cuisine", "jardin": "le jardin", "chambre": "la chambre"}
    time_np = {"matin": "le matin", "sieste": "après la sieste", "soir": "le soir"}
    fin_image = {
        "matin": "Le pain a une miette encore chaude.",
        "sieste": "La couverture retombe, tout doux.",
        "soir": "La lampe reste allumée, un moment.",
    }

    def l3(place: str, toy: str, t: str) -> list[tuple[str, str]]:
        return time_open[t] + [
            ("narrateur", extras_l3[(place, toy, t)]),
            ("narrateur", f"Nina se souvient de {place_np[place]}."),
            ("narrateur", f"Elle a encore {toy_np[toy]} tout près."),
            ("enfant-f", "J'ai levé la main."),
            ("enfant-f", "J'ai attendu."),
            ("enfant-f", "Puis j'ai parlé."),
            ("papa", "Tu as bien fait d'attendre."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo, Nina."),
            ("papa", "C'est du bon travail."),
            ("enfant-f", "Merci, papa."),
            ("enfant-f", "Merci, maman."),
            ("narrateur", "Nina range un tout petit peu, tout doux."),
        ]

    def fin(place: str, toy: str, t: str) -> list[tuple[str, str]]:
        return [
            ("enfant-f", "J'ai attendu."),
            ("enfant-f", "Puis j'ai parlé."),
            ("maman", "Bravo, Nina."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Nina a choisi {place_np[place]}, {toy_np[toy]}, et {time_np[t]}."),
            ("narrateur", fin_image[t]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois jeux attendent, tout proches."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
            ("papa", "On joue."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Le jour a trois moments tout calmes."),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
            ("maman", "On t'écoute."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "La gouttière fait un petit chant, tout mouillé."),
        ("narrateur", "Une goutte glisse sur le carreau."),
        ("narrateur", "Elle laisse un trait, tout brillant."),
        ("narrateur", "La soupe fume dans la casserole."),
        ("narrateur", "Ça sent la carotte, toute douce."),
        ("narrateur", "Les bottes de Nina sèchent près de la porte."),
        ("narrateur", "Elles sont encore brillantes, un peu froides."),
        ("narrateur", "Papa tourne la cuillère en bois."),
        ("narrateur", "Le bois est lisse, un peu chaud."),
        ("narrateur", "Maman essuie la table."),
        ("narrateur", "Le torchon est rayé, un peu rêche."),
        ("papa", "Nina, tu as vu la goutte ?"),
        ("enfant-f", "Elle descend tout doucement."),
        ("maman", "Oui."),
        ("maman", "Elle fait un trait sur le carreau."),
        ("narrateur", "En ce moment, Nina a une chose à dire."),
        ("narrateur", "Elle se tient près de la table."),
        ("narrateur", "Papa parle encore, tout doucement."),
        ("enfant-f", "J'ai une chose."),
        ("papa", "On attend."),
        ("papa", "Puis on parle."),
        ("maman", "Tu peux lever la main."),
        ("narrateur", "Nina lève la main."),
        ("narrateur", "Elle attend."),
        ("narrateur", "Une autre goutte tombe, loin, dans l'évier."),
    ]
    sons["CHK_T0000_P0000"] = "goutte,soupe"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "La maison a trois coins tout proches."),
        ("papa", "La cuisine, le jardin, ou la chambre ?"),
        ("maman", "On s'assoit."),
        ("maman", "On attend."),
        ("maman", "Puis on parle."),
    ]
    sons["CHK_T0001_P0000"] = ""

    toy_sons = {"cubes": "cubes", "livre": "", "dinette": "assiette"}
    place_sons = {"cuisine": "soupe", "jardin": "oiseau", "chambre": ""}

    for p1, place in places.items():
        by[f"CHK_T0001_{p1}"] = place_l1[place]
        by[f"CHK_T0001_{p1}_Q0001"] = q[place]
        by[f"CHK_T0001_{p1}_C0001"] = conf[place]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = place_sons[place]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, toy in toys.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_toy[(place, toy)]
            by[cid_l2] = toy_scene[toy] + [
                ("narrateur", extra),
                ("narrateur", f"{place_np[place].capitalize()} reste tout près."),
                ("papa", "On attend."),
                ("papa", "Puis on parle."),
            ]
            sons[cid_l2] = toy_sons[toy]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, t in times.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(place, toy, t)
                by[f"{cid_l3}_F0001"] = fin(place, toy, t)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-025",
        {
            "fil_rouge": "La gouttière chante. Nina a une chose à dire. Elle lève la main, elle attend, puis elle parle, avec papa et maman.",
            "title": "La gouttière et la main de Nina",
            "characters": "Nina, papa, maman",
            "setting": "maison sous la pluie, cuisine, jardin, chambre",
        },
        by,
        sons,
    )


def story_026() -> None:
    places = {"P0001": "tapis", "P0002": "table", "P0003": "fenetre"}
    acts = {"P0001": "histoire", "P0002": "chanson", "P0003": "dessin"}
    pels = {"P0001": "Lea", "P0002": "Tom", "P0003": "Sami"}

    place_np = {"tapis": "le tapis", "table": "la table", "fenetre": "la fenêtre"}
    act_np = {"histoire": "l'histoire", "chanson": "la chanson", "dessin": "le dessin"}
    pel_info = {
        "Lea": ("Léa", "la poupée Léa", "poupée"),
        "Tom": ("Tom", "l'ours Tom", "ours"),
        "Sami": ("Sami", "le lion Sami", "lion"),
    }

    place_l1 = {
        "tapis": [
            ("narrateur", "Aniss s'assoit sur le tapis gris."),
            ("narrateur", "Le tapis est un peu rêche, tout chaud."),
            ("narrateur", "Un fil dépasse, tout doux."),
            ("narrateur", "Papa pose un coussin, tout près."),
            ("papa", "Moi, je raconte le tapis."),
            ("narrateur", "Papa parle jusqu'au bout."),
            ("narrateur", "Aniss a une idée."),
            ("narrateur", "Il lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "C'est mon tour ?"),
            ("papa", "Oui."),
            ("papa", "C'est ton tour."),
            ("papa", "On a attendu."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss parle, tout doucement."),
            ("enfant-m", "Le tapis chatouille un peu."),
            ("maman", "Bravo, Aniss."),
            ("maman", "Tu as levé la main."),
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", "Le fil doux reste sous le genou."),
            ("papa", "On peut lever la main, encore."),
        ],
        "table": [
            ("narrateur", "Aniss tire une chaise près de la table."),
            ("narrateur", "Le bois est lisse, un peu froid."),
            ("narrateur", "Un crayon bleu roule, tout lentement."),
            ("narrateur", "Une feuille blanche attend, toute plate."),
            ("maman", "Assieds-toi, Aniss."),
            ("maman", "Moi, je raconte le crayon."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "Le crayon est bleu."),
            ("papa", "Oui."),
            ("papa", "Merci d'avoir attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss pose la main à plat, tout calme."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
            ("maman", "Puis tu as parlé."),
            ("narrateur", "Le crayon bleu reste près de la feuille."),
            ("papa", "On peut lever la main, à la table aussi."),
        ],
        "fenetre": [
            ("narrateur", "Aniss s'approche de la fenêtre."),
            ("narrateur", "La vitre est embuée, tout bas."),
            ("narrateur", "Une goutte dessine un trait, tout brillant."),
            ("narrateur", "Dehors, un toit brille, tout mouillé."),
            ("papa", "Regarde, Aniss."),
            ("papa", "Moi, je raconte la goutte."),
            ("narrateur", "Papa parle, tout calme."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("enfant-m", "La goutte descend tout doucement."),
            ("maman", "Oui."),
            ("maman", "C'est ton tour."),
            ("maman", "On a attendu."),
            ("maman", "Puis on parle."),
            ("narrateur", "Aniss trace un rond sur la buée, tout léger."),
            ("papa", "Bravo, Aniss."),
            ("papa", "Tu as attendu."),
            ("papa", "Puis tu as parlé."),
            ("narrateur", "Le rond s'efface, tout lentement."),
            ("maman", "On peut lever la main, près de la fenêtre aussi."),
        ],
    }

    q = {
        "tapis": [
            ("narrateur", "Sur le tapis, Aniss veut parler."),
            ("papa", "Il fait quoi d'abord ?"),
        ],
        "table": [
            ("narrateur", "À la table, Aniss veut parler."),
            ("maman", "Il fait quoi d'abord ?"),
        ],
        "fenetre": [
            ("narrateur", "Près de la fenêtre, Aniss veut parler."),
            ("papa", "Il fait quoi d'abord ?"),
        ],
    }

    conf = {
        "tapis": [
            ("papa", "Oui."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss souffle un peu."),
            ("narrateur", "Sa main redescend, tout doux."),
            ("narrateur", "Le tapis reste chaud sous les genoux."),
            ("enfant-m", "J'ai attendu."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
            ("papa", "C'est du bon travail, Aniss."),
            ("narrateur", "Le fil doux chatouille encore."),
            ("maman", "Tu as parlé, après avoir attendu."),
        ],
        "table": [
            ("maman", "Oui."),
            ("maman", "On lève la main."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Aniss pose le crayon, tout droit."),
            ("narrateur", "La feuille est encore blanche, toute plate."),
            ("enfant-m", "J'ai levé la main."),
            ("papa", "Bravo, Aniss."),
            ("papa", "Tu as attendu ton tour."),
            ("narrateur", "Le bois de la table est un peu froid."),
            ("maman", "C'est du bon travail."),
            ("maman", "On continue ensemble."),
        ],
        "fenetre": [
            ("papa", "Oui."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss essuie un peu de buée, tout doux."),
            ("narrateur", "Le toit mouillé brille encore."),
            ("enfant-m", "J'ai attendu."),
            ("enfant-m", "Puis j'ai parlé."),
            ("maman", "Bravo."),
            ("maman", "Tu as levé la main."),
            ("papa", "C'est du bon travail, Aniss."),
            ("narrateur", "Une autre goutte glisse, tout loin."),
            ("maman", "On peut lever la main, encore."),
        ],
    }

    act_scene = {
        "histoire": [
            ("narrateur", "Maman ouvre un petit livre."),
            ("narrateur", "La page sent le papier, tout sec."),
            ("narrateur", "Un lapin blanc est dessiné, tout rond."),
            ("maman", "Moi, je raconte le lapin."),
            ("narrateur", "Maman parle jusqu'au bout."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("maman", "C'est ton tour, Aniss."),
            ("enfant-m", "Le lapin a de grandes oreilles."),
            ("papa", "Oui."),
            ("papa", "Merci d'avoir attendu."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Aniss touche la page, tout léger."),
            ("papa", "Bravo."),
        ],
        "chanson": [
            ("narrateur", "Papa fredonne tout bas."),
            ("narrateur", "La voix est ronde, tout calme."),
            ("narrateur", "Aniss tapote le genou, tout doux."),
            ("papa", "Moi, je chante d'abord."),
            ("narrateur", "Papa chante jusqu'au bout."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("papa", "C'est ton tour."),
            ("enfant-m", "Je connais la chanson."),
            ("maman", "Oui."),
            ("maman", "Tu as attendu."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
            ("narrateur", "Aniss chante un tout petit bout."),
            ("maman", "Bravo, Aniss."),
        ],
        "dessin": [
            ("narrateur", "Aniss prend un crayon bleu."),
            ("narrateur", "Le bois est lisse, un peu chaud."),
            ("narrateur", "Une feuille attend, toute blanche."),
            ("maman", "Moi, je dessine d'abord un rond."),
            ("narrateur", "Maman parle, et elle dessine."),
            ("narrateur", "Aniss lève la main."),
            ("narrateur", "Il attend."),
            ("maman", "C'est ton tour."),
            ("enfant-m", "Je dessine une maison."),
            ("papa", "Oui."),
            ("papa", "Merci d'avoir attendu."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("narrateur", "Aniss trace un toit, tout doux."),
            ("papa", "Bravo."),
        ],
    }

    extra_act = {
        ("tapis", "histoire"): "Le lapin blanc semble assis sur le tapis gris.",
        ("tapis", "chanson"): "La chanson fait un petit écho, tout bas, sur le tapis.",
        ("tapis", "dessin"): "Le crayon bleu roule un peu, sur le tapis rêche.",
        ("table", "histoire"): "Le livre est ouvert, tout plat, sur la table.",
        ("table", "chanson"): "Le crayon bleu tapote la table, en rythme.",
        ("table", "dessin"): "La maison bleue grandit, sur la feuille blanche.",
        ("fenetre", "histoire"): "Le lapin blanc regarde la goutte, sur la vitre.",
        ("fenetre", "chanson"): "La chanson suit la goutte, tout lentement.",
        ("fenetre", "dessin"): "La maison bleue a une fenêtre, comme la vraie.",
    }

    peluche = {
        "Lea": [
            ("narrateur", "Aniss rejoint la poupée Léa."),
            ("narrateur", "La robe est bleue, un peu froissée."),
            ("narrateur", "Un bouton brille, tout petit."),
            ("narrateur", "Aniss l'assoit contre le coussin."),
            ("enfant-m", "Léa, j'ai levé la main."),
            ("enfant-m", "J'ai attendu."),
            ("maman", "Tu peux le dire à Léa."),
            ("maman", "Papa et maman t'écoutent aussi."),
            ("narrateur", "Aniss lisse la robe bleue."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ],
        "Tom": [
            ("narrateur", "Aniss rejoint l'ours Tom."),
            ("narrateur", "L'ours est brun, un peu râpé."),
            ("narrateur", "Une oreille est plus douce que l'autre."),
            ("narrateur", "Aniss l'assoit tout droit."),
            ("enfant-m", "Tom, j'ai attendu."),
            ("enfant-m", "Puis j'ai parlé."),
            ("papa", "Tu as bien fait."),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("narrateur", "Aniss caresse l'oreille de l'ours."),
            ("maman", "Bravo, Aniss."),
        ],
        "Sami": [
            ("narrateur", "Aniss rejoint le lion Sami."),
            ("narrateur", "La crinière est en laine, un peu mêlée."),
            ("narrateur", "Un œil de bouton regarde, tout calme."),
            ("narrateur", "Aniss tient Sami contre son genou."),
            ("enfant-m", "Sami, j'ai levé la main."),
            ("maman", "Tu as attendu."),
            ("maman", "Puis tu as parlé."),
            ("maman", "Je t'écoute."),
            ("narrateur", "Aniss range une mèche de laine."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ],
    }

    extra_pel = {
        ("tapis", "histoire", "Lea"): "La poupée Léa a un lapin blanc, collé au tablier.",
        ("tapis", "histoire", "Tom"): "L'ours Tom a une page du livre, sous la patte.",
        ("tapis", "histoire", "Sami"): "Le lion Sami écoute le lapin, tout sage.",
        ("tapis", "chanson", "Lea"): "La poupée Léa a un grelot, tout petit.",
        ("tapis", "chanson", "Tom"): "L'ours Tom tapote le tapis, en rythme.",
        ("tapis", "chanson", "Sami"): "Le lion Sami a la crinière qui bouge, tout doux.",
        ("tapis", "dessin", "Lea"): "La poupée Léa a un trait bleu, sur la robe.",
        ("tapis", "dessin", "Tom"): "L'ours Tom a un crayon, trop grand, sous le bras.",
        ("tapis", "dessin", "Sami"): "Le lion Sami a une maison bleue, sur le ventre.",
        ("table", "histoire", "Lea"): "La poupée Léa est assise près du livre, tout droite.",
        ("table", "histoire", "Tom"): "L'ours Tom pose le nez sur le lapin blanc.",
        ("table", "histoire", "Sami"): "Le lion Sami a une miette de papier, dans la laine.",
        ("table", "chanson", "Lea"): "La poupée Léa se balance, tout léger, sur la chaise.",
        ("table", "chanson", "Tom"): "L'ours Tom a l'oreille pliée, comme une note.",
        ("table", "chanson", "Sami"): "Le lion Sami écoute la table, tout calme.",
        ("table", "dessin", "Lea"): "La poupée Léa tient le crayon bleu, trop lourd.",
        ("table", "dessin", "Tom"): "L'ours Tom a un rond bleu, sur la patte.",
        ("table", "dessin", "Sami"): "Le lion Sami veille près de la feuille blanche.",
        ("fenetre", "histoire", "Lea"): "La poupée Léa regarde la goutte, tout près.",
        ("fenetre", "histoire", "Tom"): "L'ours Tom a un peu de buée, sur le nez.",
        ("fenetre", "histoire", "Sami"): "Le lion Sami suit le trait sur la vitre.",
        ("fenetre", "chanson", "Lea"): "La poupée Léa a une goutte, sur le bouton.",
        ("fenetre", "chanson", "Tom"): "L'ours Tom écoute la pluie, tout brun.",
        ("fenetre", "chanson", "Sami"): "Le lion Sami a la crinière un peu humide.",
        ("fenetre", "dessin", "Lea"): "La poupée Léa a une maison, près de la vitre.",
        ("fenetre", "dessin", "Tom"): "L'ours Tom a un toit bleu, comme dehors.",
        ("fenetre", "dessin", "Sami"): "Le lion Sami a un rond de buée, sur la laine.",
    }

    fin_image = {
        "Lea": "La poupée Léa s'endort contre le coussin.",
        "Tom": "L'ours Tom baisse une oreille, tout doux.",
        "Sami": "Le lion Sami ferme un œil de bouton.",
    }

    def l3(place: str, act: str, pel: str) -> list[tuple[str, str]]:
        _, pel_np, _ = pel_info[pel]
        return peluche[pel] + [
            ("narrateur", extra_pel[(place, act, pel)]),
            ("narrateur", f"Aniss se souvient de {place_np[place]}."),
            ("narrateur", f"Il a vécu {act_np[act]}, tout près."),
            ("enfant-m", "J'ai levé la main."),
            ("enfant-m", "J'ai attendu."),
            ("enfant-m", "Puis j'ai parlé."),
            ("papa", "Tu as bien fait d'attendre."),
            ("maman", "On attend."),
            ("maman", "Puis on parle."),
            ("papa", "Bravo, Aniss."),
            ("papa", "C'est du bon travail."),
            ("enfant-m", "Merci, papa."),
            ("enfant-m", "Merci, maman."),
            ("narrateur", f"Aniss pose {pel_np}, tout doux."),
        ]

    def fin(place: str, act: str, pel: str) -> list[tuple[str, str]]:
        return [
            ("enfant-m", "J'ai attendu."),
            ("enfant-m", "Puis j'ai parlé."),
            ("maman", "Bravo, Aniss."),
            ("papa", "Tu as fait du bon travail."),
            ("narrateur", f"Aniss a choisi {place_np[place]}, {act_np[act]}, et {pel_info[pel][1]}."),
            ("narrateur", fin_image[pel]),
            ("narrateur", "L'histoire est finie."),
        ]

    def trans_l2() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Le coin école a trois envies."),
            ("maman", "L'histoire, la chanson, ou le dessin ?"),
            ("papa", "On lève la main."),
            ("papa", "On attend."),
            ("papa", "Puis on parle."),
        ]

    def trans_l3() -> list[tuple[str, str]]:
        return [
            ("narrateur", "Trois peluches attendent, tout calmes."),
            ("papa", "Léa, Tom, ou Sami ?"),
            ("maman", "On dit bonjour."),
            ("maman", "Chacun son tour."),
        ]

    by: dict[str, list[tuple[str, str]]] = {}
    sons: dict[str, str] = {}

    by["CHK_T0000_P0000"] = [
        ("narrateur", "Le manteau d'Aniss pend au dossier, encore un peu humide."),
        ("narrateur", "Une craie blanche attend sur l'ardoise."),
        ("narrateur", "Elle laisse une poussière, toute fine."),
        ("narrateur", "Dehors, la pluie dessine des ronds sur la vitre."),
        ("narrateur", "La vitre est embuée, tout bas."),
        ("narrateur", "Papa pose trois coussins sur le tapis."),
        ("narrateur", "Le tapis est gris, un peu rêche."),
        ("narrateur", "Maman ouvre le volet, tout doux."),
        ("narrateur", "Un rectangle de lumière tombe sur la table."),
        ("maman", "Aniss, on fait l'école, ici ?"),
        ("enfant-m", "Oui."),
        ("papa", "On s'assoit."),
        ("papa", "On attend."),
        ("papa", "Puis on parle."),
        ("narrateur", "En ce moment, Aniss a une idée."),
        ("narrateur", "Il se tient près de l'ardoise."),
        ("narrateur", "La craie est froide dans sa main."),
        ("narrateur", "Papa parle déjà, tout calme."),
        ("enfant-m", "J'ai une idée."),
        ("maman", "Tu lèves la main."),
        ("maman", "Tu attends."),
        ("maman", "Puis tu parles."),
        ("narrateur", "Aniss lève la main."),
        ("narrateur", "Il attend."),
        ("narrateur", "Une goutte glisse encore, sur la vitre."),
    ]
    sons["CHK_T0000_P0000"] = "pluie,craie"

    by["CHK_T0001_P0000"] = [
        ("narrateur", "Le coin école a trois places."),
        ("papa", "Le tapis, la table, ou la fenêtre ?"),
        ("maman", "On s'assoit."),
        ("maman", "On attend."),
        ("maman", "Puis on parle."),
    ]
    sons["CHK_T0001_P0000"] = ""

    place_sons = {"tapis": "", "table": "crayon", "fenetre": "goutte"}
    act_sons = {"histoire": "livre", "chanson": "chanson", "dessin": "crayon"}

    for p1, place in places.items():
        by[f"CHK_T0001_{p1}"] = place_l1[place]
        by[f"CHK_T0001_{p1}_Q0001"] = q[place]
        by[f"CHK_T0001_{p1}_C0001"] = conf[place]
        by[f"CHK_T0001_{p1}_T0002_P0000"] = trans_l2()
        sons[f"CHK_T0001_{p1}"] = place_sons[place]
        sons[f"CHK_T0001_{p1}_Q0001"] = ""
        sons[f"CHK_T0001_{p1}_C0001"] = ""
        sons[f"CHK_T0001_{p1}_T0002_P0000"] = ""

        for p2, act in acts.items():
            cid_l2 = f"CHK_T0001_{p1}_T0002_{p2}"
            extra = extra_act[(place, act)]
            by[cid_l2] = act_scene[act] + [
                ("narrateur", extra),
                ("narrateur", f"{place_np[place].capitalize()} reste tout près."),
                ("papa", "On attend."),
                ("papa", "Puis on parle."),
            ]
            sons[cid_l2] = act_sons[act]
            by[f"{cid_l2}_T0003_P0000"] = trans_l3()
            sons[f"{cid_l2}_T0003_P0000"] = ""

            for p3, pel in pels.items():
                cid_l3 = f"{cid_l2}_T0003_{p3}"
                by[cid_l3] = l3(place, act, pel)
                by[f"{cid_l3}_F0001"] = fin(place, act, pel)
                sons[cid_l3] = ""
                sons[f"{cid_l3}_F0001"] = ""

    write_story(
        "TREE-COL-026",
        {
            "fil_rouge": "Sur l'ardoise, Aniss a une idée. Il lève la main, il attend, puis il parle, au coin école, avec papa et maman.",
            "title": "L'ardoise et la main d'Aniss",
            "characters": "Aniss, papa, maman",
            "setting": "coin école à la maison, tapis, table, fenêtre",
        },
        by,
        sons,
    )


if __name__ == "__main__":
    story_025()
    story_026()
    print("ok TREE-COL-025 TREE-COL-026")
