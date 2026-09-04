#!/usr/bin/env python3
"""F-NAR-010…015 — texte TREE-AUT-001. Générateur one-shot, pas un gabarit produit."""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = json.loads((HERE / "source.json").read_text(encoding="utf-8"))
BY = {c["chunk_id"]: c for c in SRC["chunks"]}


def pack(cid: str, lines: list[tuple[str, str]]) -> dict:
    src = BY[cid]
    script = "\n".join(f"{r}|{p}" for r, p in lines)
    text = " ".join(p for _, p in lines)
    return {
        "chunk_id": cid,
        "kind": src["kind"],
        "text": text,
        "script": script,
        "sons": src.get("sons") or "",
        "length_scale_piper": src.get("length_scale_piper") or 1.28,
        "rate_label": src.get("rate_label") or "slow",
        "pause_after_ms": src.get("pause_after_ms"),
    }


# ---------------------------------------------------------------------------
# Fil : Amir veut aller jouer. Le sac est vide. Il demande, il met, il part.
# Leçon greffée : il met ce que papa ou maman a nommé. Pas de slogan.
# ---------------------------------------------------------------------------

CHUNKS: list[dict] = []

CHUNKS.append(
    pack(
        "CHK_T0000_P0000",
        [
            ("narrateur", "Sur le toit, la gouttière fait encore plic ploc."),
            ("narrateur", "La pluie vient de s'arrêter."),
            ("narrateur", "La maison a un volet jaune."),
            ("narrateur", "Le volet claque tout doux."),
            ("narrateur", "Dans la rue, les pavés brillent."),
            ("narrateur", "Ils sont encore mouillés."),
            ("narrateur", "Une odeur de soupe entre par la fenêtre."),
            ("narrateur", "Le tapis de la chambre est rayé."),
            ("narrateur", "Il est bleu et crème."),
            ("narrateur", "Un rayon de soleil touche le plancher."),
            ("narrateur", "Papa pose un pull sur le lit."),
            ("papa", "Il est encore un peu chaud."),
            ("narrateur", "Maman ouvre un peu la fenêtre."),
            ("maman", "Tu as senti la soupe ?"),
            ("enfant-m", "Oui, maman."),
            ("narrateur", "En ce moment, Amir veut aller jouer."),
            ("narrateur", "Son sac attend sur le tapis."),
            ("narrateur", "Amir tire la fermeture."),
            ("narrateur", "Ça fait zzz."),
            ("narrateur", "Le sac est vide."),
            ("enfant-m", "Je veux jouer !"),
            ("maman", "D'accord."),
            ("maman", "On prépare ton sac d'abord."),
            ("papa", "Tu mets quoi, Amir ?"),
            ("enfant-m", "Je ne sais pas."),
            ("maman", "Demande. On t'aide."),
            ("narrateur", "Amir pose la main sur le sac."),
        ],
    )
)

CHUNKS.append(
    pack(
        "CHK_T0001_P0000",
        [
            ("narrateur", "Pour le goûter, on peut choisir."),
            ("narrateur", "Une pomme, un yaourt, ou un morceau de pain."),
        ],
    )
)

# --- pomme -----------------------------------------------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0001",
        [
            ("narrateur", "Dans la coupe, une pomme rouge brille."),
            ("narrateur", "Elle sent le fruit."),
            ("narrateur", "Amir tend la main."),
            ("narrateur", "La pomme roule sur la table."),
            ("narrateur", "Il la rattrape contre son ventre."),
            ("narrateur", "La peau est lisse et froide."),
            ("maman", "Celle-là, dans le sac."),
            ("enfant-m", "La pomme."),
            ("narrateur", "Amir la glisse au fond."),
            ("narrateur", "Le sac fait un petit toc."),
            ("maman", "Elle est bien au fond ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Ça sent encore le fruit."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_Q0001",
        [("narrateur", "On met quoi dans le sac ?")],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_C0001",
        [
            ("narrateur", "La pomme est dans le sac."),
            ("narrateur", "Elle fait un petit rond."),
            ("narrateur", "Amir touche la fermeture."),
            ("maman", "Pas encore."),
            ("maman", "Il manque encore des choses."),
            ("enfant-m", "Quoi ?"),
            ("maman", "On va voir ensemble."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0000",
        [
            ("narrateur", "On peut aller où ?"),
            ("narrateur", "La cuisine, le jardin, ou la chambre."),
        ],
    )
)

# pomme + cuisine
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001",
        [
            ("narrateur", "Amir emporte le sac vers la cuisine."),
            ("narrateur", "Le carrelage est un peu froid."),
            ("narrateur", "La soupe fume encore dans la casserole."),
            ("narrateur", "Une serviette dépasse sous une cuillère."),
            ("narrateur", "Amir tire le coin tout doux."),
            ("maman", "La petite serviette, dans le sac."),
            ("enfant-m", "La serviette."),
            ("narrateur", "Elle est douce et pliée."),
            ("narrateur", "Il la glisse près de la pomme."),
            ("maman", "Tu as fini de la mettre ?"),
            ("enfant-m", "Oui, maman."),
            ("narrateur", "Une miette reste sur la table."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0001",
        [
            ("narrateur", "Les cubes bleus attendent près de l'assiette."),
            ("narrateur", "Ils tapent un peu sur le bois."),
            ("narrateur", "Amir en empile deux."),
            ("narrateur", "La tour penche vers la pomme."),
            ("maman", "Deux cubes dans le sac."),
            ("enfant-m", "Deux cubes."),
            ("narrateur", "Il défait la tour tout doux."),
            ("narrateur", "Il les glisse près de la pomme."),
            ("papa", "Ils tiennent ?"),
            ("enfant-m", "Ils tiennent."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0001_F0001",
        [
            ("narrateur", "Amir ferme le sac près de la table."),
            ("narrateur", "Ça fait zzz."),
            ("papa", "Le sac est prêt."),
            ("enfant-m", "On peut jouer ?"),
            ("maman", "Oui. Les cubes, après."),
            ("narrateur", "Amir sort un cube."),
            ("narrateur", "Il le pose sur la table."),
            ("narrateur", "Toc."),
            ("narrateur", "La cuisine sent encore la soupe."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0002",
        [
            ("narrateur", "Un petit livre est posé près du sel."),
            ("narrateur", "Les pages sentent le papier."),
            ("narrateur", "Une page colle un peu."),
            ("narrateur", "Amir souffle dessus."),
            ("papa", "Le livre, à plat dans le sac."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le glisse près de la pomme."),
            ("papa", "Il est à plat ?"),
            ("enfant-m", "À plat."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0002_F0001",
        [
            ("narrateur", "Amir appuie sur la fermeture."),
            ("maman", "Tu as mis le livre."),
            ("papa", "Et la pomme."),
            ("enfant-m", "Le sac est prêt."),
            ("maman", "On ouvre juste la couverture ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Amir montre un bateau sur la page."),
            ("narrateur", "Puis il referme le sac."),
            ("narrateur", "Ils restent un moment près de la table."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0003",
        [
            ("narrateur", "La petite tasse de dînette cliquette."),
            ("narrateur", "Elle est rouge, près de l'évier."),
            ("narrateur", "Une goutte brille au fond."),
            ("narrateur", "Amir la verse dans l'évier."),
            ("maman", "La tasse, dans le sac."),
            ("enfant-m", "La tasse."),
            ("narrateur", "Il la pose tout doux près de la pomme."),
            ("narrateur", "Ça sonne comme un tout petit verre."),
            ("maman", "On fera la dînette après."),
            ("enfant-m", "Oui, maman."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0003_F0001",
        [
            ("narrateur", "Le sac a la pomme et la tasse."),
            ("narrateur", "Amir le serre contre lui."),
            ("papa", "On va jouer ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Il sort la tasse."),
            ("narrateur", "Il fait semblant de boire."),
            ("maman", "À plus tard, petite tasse."),
            ("narrateur", "Une goutte tombe dans l'évier."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# pomme + jardin
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002",
        [
            ("narrateur", "Amir pousse la porte du jardin."),
            ("narrateur", "L'herbe est encore mouillée."),
            ("narrateur", "Une feuille colle à sa chaussette."),
            ("narrateur", "Un petit linge sèche sur le banc."),
            ("papa", "Le petit linge, Amir."),
            ("papa", "On le met dans le sac."),
            ("enfant-m", "Le linge."),
            ("narrateur", "Le linge sent l'air frais."),
            ("narrateur", "Amir le pose près de la pomme."),
            ("narrateur", "Un oiseau chante sur le mur."),
            ("papa", "Tu as entendu l'oiseau ?"),
            ("enfant-m", "Oui, papa."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0001",
        [
            ("narrateur", "Les cubes sont sur la pierre chaude."),
            ("narrateur", "Ils sentent un peu le soleil."),
            ("narrateur", "Un cube a une goutte dessus."),
            ("narrateur", "Amir l'essuie sur son pantalon."),
            ("papa", "Un cube dans le sac."),
            ("enfant-m", "Un cube."),
            ("narrateur", "Il le met près de la pomme."),
            ("narrateur", "Une abeille passe, tout loin."),
            ("papa", "On laisse l'abeille au jardin."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0001_F0001",
        [
            ("narrateur", "Amir referme le sac sur l'herbe."),
            ("enfant-m", "C'est prêt."),
            ("papa", "On enlève la feuille, d'abord."),
            ("narrateur", "Amir ôte la feuille de sa chaussette."),
            ("narrateur", "Il sort le cube."),
            ("narrateur", "Il le pose sur la pierre."),
            ("maman", "On rentre quand tu veux."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0002",
        [
            ("narrateur", "Le livre est à l'ombre, sous le banc."),
            ("narrateur", "L'herbe chatouille les chevilles."),
            ("narrateur", "Amir se penche."),
            ("narrateur", "Les pages sont un peu fraîches."),
            ("maman", "Le livre dans le sac, Amir."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le glisse près de la pomme."),
            ("maman", "On lira plus tard, au calme."),
            ("enfant-m", "D'accord."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac est posé sur le banc."),
            ("narrateur", "Amir ouvre un tout petit coin."),
            ("narrateur", "Il regarde une page."),
            ("papa", "On rentre avec le sac."),
            ("enfant-m", "Oui."),
            ("narrateur", "Un oiseau s'envole du mur."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0003",
        [
            ("narrateur", "La dînette est sur un linge, dans l'herbe."),
            ("narrateur", "Une assiette minuscule brille."),
            ("narrateur", "Une feuille sèche est posée dessus."),
            ("narrateur", "Amir enlève la feuille."),
            ("maman", "L'assiette dans le sac, Amir."),
            ("enfant-m", "L'assiette."),
            ("narrateur", "Il la pose à plat près de la pomme."),
            ("papa", "Elle est à plat ?"),
            ("enfant-m", "Oui."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0003_F0001",
        [
            ("narrateur", "Amir tient le sac contre lui."),
            ("enfant-m", "Le sac est prêt."),
            ("maman", "On goûte la pomme dehors ?"),
            ("enfant-m", "Après."),
            ("narrateur", "Il sort l'assiette."),
            ("narrateur", "Il pose la pomme dessus, un instant."),
            ("narrateur", "Puis tout rentre dans le sac."),
            ("narrateur", "Une goutte tombe de la gouttière."),
            ("narrateur", "Plic ploc."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# pomme + chambre
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003",
        [
            ("narrateur", "Amir revient dans la chambre."),
            ("narrateur", "Le tapis rayé est tiède."),
            ("narrateur", "Le pull marine attend sur le lit."),
            ("narrateur", "Amir essaie de le plier."),
            ("narrateur", "Une manche dépasse."),
            ("papa", "Le pull, dans le sac."),
            ("enfant-m", "Le pull."),
            ("narrateur", "Il le tasse près de la pomme."),
            ("papa", "La manche est rentrée ?"),
            ("enfant-m", "Presque."),
            ("narrateur", "Le volet claque encore un peu."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0001",
        [
            ("narrateur", "Les cubes sont sous la chaise."),
            ("narrateur", "Un cube rouge a roulé loin."),
            ("narrateur", "Amir rampe sur le tapis."),
            ("narrateur", "Il rattrape le cube rouge."),
            ("maman", "Les cubes dans le sac."),
            ("enfant-m", "Les cubes."),
            ("narrateur", "Il les met près de la pomme."),
            ("maman", "Tu as le rouge ?"),
            ("enfant-m", "Oui."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0001_F0001",
        [
            ("narrateur", "Amir ferme le sac au pied du lit."),
            ("enfant-m", "On peut jouer ?"),
            ("papa", "Oui. Sur le tapis."),
            ("narrateur", "Amir sort deux cubes."),
            ("narrateur", "Il les pose sur une rayure crème."),
            ("narrateur", "Le tapis rayé est calme."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0002",
        [
            ("narrateur", "Le livre est ouvert sur la commode."),
            ("narrateur", "Une image montre un bateau."),
            ("narrateur", "Amir le ferme tout doux."),
            ("papa", "Le livre dans le sac, Amir."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le glisse près de la pomme."),
            ("papa", "Le bateau est dedans aussi."),
            ("enfant-m", "Oui."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac est sur la commode, une seconde."),
            ("maman", "On va jouer ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Amir ouvre le sac."),
            ("narrateur", "Il touche la couverture du livre."),
            ("narrateur", "Le rayon de soleil a quitté le tapis."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0003",
        [
            ("narrateur", "La dînette est dans la caisse, sous le lit."),
            ("narrateur", "Une petite assiette dépasse."),
            ("narrateur", "Amir tire l'assiette."),
            ("narrateur", "Un couvercle tombe sur le tapis."),
            ("narrateur", "Toc."),
            ("maman", "L'assiette dans le sac."),
            ("enfant-m", "L'assiette."),
            ("narrateur", "Il la met près de la pomme."),
            ("maman", "Le couvercle, on le laisse."),
            ("enfant-m", "D'accord."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0003_F0001",
        [
            ("narrateur", "Amir s'assoit sur le tapis."),
            ("narrateur", "Le sac est sur ses genoux."),
            ("papa", "Le sac est prêt."),
            ("enfant-m", "Merci."),
            ("narrateur", "Il sort l'assiette."),
            ("narrateur", "Il y pose la pomme, pour rire."),
            ("maman", "On va vraiment jouer, maintenant."),
            ("narrateur", "La couverture retombe sur le lit."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# --- yaourt ----------------------------------------------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0002",
        [
            ("narrateur", "Papa ouvre le frigo."),
            ("narrateur", "Un air frais sort."),
            ("narrateur", "Un petit yaourt attend sur la tablette."),
            ("narrateur", "Papa le tend."),
            ("narrateur", "Le couvercle glisse un peu."),
            ("narrateur", "Amir le tient à deux mains."),
            ("papa", "Tout doux. Dans le sac."),
            ("enfant-m", "Le yaourt."),
            ("narrateur", "Amir le pose bien droit."),
            ("papa", "Il tient ?"),
            ("enfant-m", "Il tient."),
            ("narrateur", "Le pot est froid contre le tissu."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_Q0001",
        [("narrateur", "On met quoi dans le sac ?")],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_C0001",
        [
            ("narrateur", "Le yaourt est au fond."),
            ("narrateur", "Il est froid."),
            ("narrateur", "Amir veut fermer le sac."),
            ("papa", "On n'a pas fini."),
            ("papa", "Il manque encore des choses."),
            ("enfant-m", "D'accord."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0000",
        [
            ("narrateur", "On peut aller où ?"),
            ("narrateur", "La cuisine, le jardin, ou la chambre."),
        ],
    )
)

# yaourt + cuisine
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001",
        [
            ("narrateur", "Amir pose le sac sur la table."),
            ("narrateur", "Le yaourt reste bien droit."),
            ("narrateur", "Le frigo ronronne tout bas."),
            ("narrateur", "Amir ouvre le tiroir du bas."),
            ("narrateur", "Une petite cuillère brille."),
            ("papa", "La cuillère, dans le sac."),
            ("enfant-m", "La cuillère."),
            ("narrateur", "Elle est lisse et froide."),
            ("narrateur", "Il la glisse à côté du yaourt."),
            ("papa", "Elle est à côté ?"),
            ("enfant-m", "Oui, papa."),
            ("narrateur", "Ça sent encore la soupe."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0001",
        [
            ("narrateur", "Les cubes sont près du saladier."),
            ("narrateur", "Amir en prend trois."),
            ("narrateur", "Il fait un petit pont."),
            ("narrateur", "Le pont touche le yaourt."),
            ("maman", "Les cubes, dans le sac. Pas le pont."),
            ("enfant-m", "Les cubes."),
            ("narrateur", "Il les empile près du pot."),
            ("maman", "Le pot est encore droit ?"),
            ("enfant-m", "Droit."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0001_F0001",
        [
            ("narrateur", "Amir ferme le sac près de l'évier."),
            ("papa", "Le yaourt est encore droit ?"),
            ("enfant-m", "Oui."),
            ("maman", "On joue aux cubes ici."),
            ("narrateur", "Amir sort deux cubes."),
            ("narrateur", "Il les pose contre la cuillère."),
            ("narrateur", "Toc, toc."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0002",
        [
            ("narrateur", "Le livre est sous un torchon."),
            ("narrateur", "Le torchon sent le propre."),
            ("narrateur", "Amir soulève le coin."),
            ("papa", "Le livre dans le sac."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le sort du torchon."),
            ("narrateur", "Il le glisse près du yaourt, à plat."),
            ("papa", "Loin du pot froid."),
            ("enfant-m", "Loin."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac est posé contre la chaise."),
            ("enfant-m", "On lit ?"),
            ("maman", "Une page. Puis on range."),
            ("narrateur", "Amir ouvre le sac."),
            ("narrateur", "Il montre la couverture à papa."),
            ("papa", "On y va."),
            ("narrateur", "Ça sent encore un peu le four."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0003",
        [
            ("narrateur", "La dînette est dans le tiroir du haut."),
            ("narrateur", "Une casserole minuscule brille."),
            ("narrateur", "Amir ouvre le tiroir tout doux."),
            ("maman", "La casserole dans le sac."),
            ("enfant-m", "La casserole."),
            ("narrateur", "Il la met près du yaourt."),
            ("narrateur", "Elle fait un tout petit cling."),
            ("maman", "On fera la soupe pour de faux."),
            ("enfant-m", "Oui."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0003_F0001",
        [
            ("narrateur", "Amir tient la sangle du sac."),
            ("papa", "Le sac est prêt."),
            ("enfant-m", "La casserole aussi."),
            ("narrateur", "Il sort la casserole."),
            ("narrateur", "Il fait semblant de remuer."),
            ("maman", "La soupe de yaourt, c'est nouveau."),
            ("narrateur", "Amir rit."),
            ("narrateur", "La cuisine est calme."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# yaourt + jardin
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002",
        [
            ("narrateur", "Amir marche dans le jardin avec le sac."),
            ("narrateur", "Le yaourt reste au fond, au frais."),
            ("narrateur", "Un galet est encore chaud au soleil."),
            ("narrateur", "Un petit gant est posé dessus."),
            ("maman", "Le petit gant, dans le sac."),
            ("enfant-m", "Le gant."),
            ("narrateur", "Le gant est un peu rêche."),
            ("narrateur", "Amir le pose près du yaourt."),
            ("narrateur", "Une goutte tombe de la gouttière."),
            ("papa", "Plic ploc. Tu as entendu ?"),
            ("enfant-m", "Oui."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0001",
        [
            ("narrateur", "Les cubes sont dans l'herbe rase."),
            ("narrateur", "Un cube a un peu d'herbe."),
            ("narrateur", "Amir souffle dessus."),
            ("papa", "Le cube propre, dans le sac."),
            ("enfant-m", "Le cube propre."),
            ("narrateur", "Il le frotte, puis le met près du yaourt."),
            ("papa", "On laisse l'herbe au jardin."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0001_F0001",
        [
            ("narrateur", "Amir referme le sac près du galet."),
            ("maman", "Le yaourt est encore au frais ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Il sort le cube."),
            ("narrateur", "Il le pose sur le galet chaud."),
            ("papa", "On rentre."),
            ("narrateur", "Le jardin sent l'herbe mouillée."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0002",
        [
            ("narrateur", "Le livre est sur le muret, au soleil."),
            ("narrateur", "La couverture est un peu chaude."),
            ("narrateur", "Amir le souffle."),
            ("maman", "Le livre dans le sac."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le glisse près du yaourt."),
            ("maman", "Pas collé au pot froid."),
            ("enfant-m", "Pas collé."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac est posé sur le muret."),
            ("enfant-m", "Une page ?"),
            ("papa", "Une page. Le vent est doux."),
            ("narrateur", "Amir ouvre le livre."),
            ("narrateur", "Une page tremble."),
            ("narrateur", "Il referme, puis le sac."),
            ("narrateur", "On rentre avec le sac."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0003",
        [
            ("narrateur", "Une tasse de dînette est retournée dans l'herbe."),
            ("narrateur", "Une goutte d'eau brille dedans."),
            ("narrateur", "Amir la vide sur l'herbe."),
            ("papa", "La tasse dans le sac."),
            ("enfant-m", "La tasse."),
            ("narrateur", "Il la met près du yaourt."),
            ("papa", "Elle est vide ?"),
            ("enfant-m", "Vide."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0003_F0001",
        [
            ("narrateur", "Amir tient le sac à deux mains."),
            ("maman", "On rentre."),
            ("enfant-m", "La tasse aussi."),
            ("narrateur", "Il fait un tout petit clin."),
            ("narrateur", "Tasse contre yaourt."),
            ("papa", "Santé, tout doux."),
            ("narrateur", "Le jardin sent l'herbe mouillée."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# yaourt + chambre
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003",
        [
            ("narrateur", "Amir s'assoit sur le tapis de la chambre."),
            ("narrateur", "Le yaourt fait un petit rond dans le sac."),
            ("narrateur", "La couverture est douce contre le genou."),
            ("narrateur", "Un chausson dépasse sous le lit."),
            ("narrateur", "Amir tire les deux chaussons."),
            ("papa", "Les chaussons, dans le sac."),
            ("enfant-m", "Les chaussons."),
            ("narrateur", "Ils sont chauds et mous."),
            ("narrateur", "Il les glisse près du yaourt."),
            ("narrateur", "Le rayon de soleil a bougé."),
            ("narrateur", "Il touche maintenant le sac."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0001",
        [
            ("narrateur", "Les cubes sont derrière le coffre."),
            ("narrateur", "Amir pousse le coffre d'un doigt."),
            ("narrateur", "Deux cubes apparaissent."),
            ("maman", "Les cubes dans le sac."),
            ("enfant-m", "Les cubes."),
            ("narrateur", "Il les met près du yaourt."),
            ("maman", "Loin du pot, un peu."),
            ("enfant-m", "Loin."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0001_F0001",
        [
            ("narrateur", "Amir ferme le sac au pied du lit."),
            ("papa", "Les chaussons et les cubes sont dedans."),
            ("enfant-m", "Le sac est prêt."),
            ("narrateur", "Il sort un cube."),
            ("narrateur", "Il le fait rouler sur une rayure bleue."),
            ("maman", "On peut jouer."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0002",
        [
            ("narrateur", "Le livre est coincé entre deux peluches."),
            ("narrateur", "Amir le tire tout doux."),
            ("papa", "Le livre dans le sac."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le glisse près du yaourt."),
            ("papa", "Les peluches restent au lit."),
            ("enfant-m", "D'accord."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac attend près de la porte."),
            ("enfant-m", "Merci, papa."),
            ("maman", "On lit sur le tapis ?"),
            ("narrateur", "Amir s'assoit."),
            ("narrateur", "Il ouvre le livre sur ses genoux."),
            ("narrateur", "Le rayon de soleil a quitté le tapis."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0003",
        [
            ("narrateur", "La dînette est dans le panier, près du lit."),
            ("narrateur", "Une tasse et une assiette s'entrechoquent."),
            ("maman", "La tasse seulement, Amir."),
            ("enfant-m", "La tasse."),
            ("narrateur", "Amir prend la tasse."),
            ("narrateur", "L'assiette reste dans le panier."),
            ("narrateur", "Il met la tasse près du yaourt."),
            ("maman", "Juste la tasse."),
            ("enfant-m", "Juste la tasse."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0003_F0001",
        [
            ("narrateur", "Amir s'assoit, le sac sur les genoux."),
            ("papa", "Le sac est prêt."),
            ("enfant-m", "Merci, maman."),
            ("narrateur", "Il sort la tasse."),
            ("narrateur", "Il fait semblant de goûter le yaourt."),
            ("maman", "Après, pour de vrai."),
            ("narrateur", "La couverture retombe sur le lit."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# --- pain ------------------------------------------------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0003",
        [
            ("narrateur", "Sur la planche, un morceau de pain attend."),
            ("narrateur", "La croûte fait un petit bruit."),
            ("narrateur", "Ça sent encore le four."),
            ("narrateur", "Une miette tombe sur le tapis."),
            ("maman", "Le pain, dans le sac."),
            ("enfant-m", "Le pain."),
            ("narrateur", "Amir le glisse contre la paroi."),
            ("narrateur", "Une miette reste sur sa manche."),
            ("narrateur", "Il souffle dessus."),
            ("maman", "Il est dedans ?"),
            ("enfant-m", "Oui, maman."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_Q0001",
        [("narrateur", "Qui a dit de mettre le pain ?")],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_C0001",
        [
            ("narrateur", "Maman a dit le pain."),
            ("narrateur", "Le pain est dans le sac."),
            ("narrateur", "Ça sent encore le four."),
            ("narrateur", "Amir tape sur le sac."),
            ("maman", "Ce n'est pas fini."),
            ("maman", "On cherche encore un peu."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0000",
        [
            ("narrateur", "On peut aller où ?"),
            ("narrateur", "La cuisine, le jardin, ou la chambre."),
        ],
    )
)

# pain + cuisine
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001",
        [
            ("narrateur", "Amir pose le sac près de l'évier."),
            ("narrateur", "Le pain sent encore le four."),
            ("narrateur", "L'eau fait un tout petit bruit."),
            ("narrateur", "Une boîte à goûter attend."),
            ("narrateur", "Elle est lisse et bleue."),
            ("maman", "La boîte, Amir."),
            ("maman", "Le pain va dedans."),
            ("enfant-m", "La boîte."),
            ("narrateur", "Amir sort le pain du sac."),
            ("narrateur", "Il le glisse dans la boîte."),
            ("narrateur", "Puis la boîte dans le sac."),
            ("maman", "Tu as fini ?"),
            ("enfant-m", "Oui, maman."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0001",
        [
            ("narrateur", "Les cubes sont près de la boîte à goûter."),
            ("narrateur", "Ils font une petite tour."),
            ("narrateur", "Amir défait la tour tout doux."),
            ("papa", "Deux cubes dans le sac."),
            ("enfant-m", "Deux cubes."),
            ("narrateur", "Il les met à côté de la boîte."),
            ("papa", "Pas dans la boîte."),
            ("enfant-m", "À côté."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0001_F0001",
        [
            ("narrateur", "Amir ferme le sac près de l'évier."),
            ("maman", "Le pain est dans la boîte."),
            ("papa", "Les cubes aussi, à côté."),
            ("enfant-m", "On a fini le sac."),
            ("narrateur", "Il sort un cube."),
            ("narrateur", "Il le pose sur le couvercle bleu."),
            ("narrateur", "L'eau ne coule plus."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0002",
        [
            ("narrateur", "Le livre est debout entre deux bocaux."),
            ("narrateur", "Amir le prend par le dos."),
            ("papa", "Le livre dans le sac."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le glisse près de la boîte."),
            ("papa", "Au-dessus du pain."),
            ("enfant-m", "Au-dessus."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac est posé contre la chaise."),
            ("enfant-m", "On va jouer."),
            ("maman", "On ouvre le livre d'abord ?"),
            ("narrateur", "Amir montre une page à maman."),
            ("narrateur", "Ça sent encore un peu le four."),
            ("papa", "On y va."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0003",
        [
            ("narrateur", "Une casserole de dînette est près du sel."),
            ("narrateur", "Le couvercle est à l'envers."),
            ("narrateur", "Amir le remet dessus."),
            ("maman", "La casserole dans le sac."),
            ("enfant-m", "La casserole."),
            ("narrateur", "Il la met près de la boîte."),
            ("maman", "On fera le pain pour de faux."),
            ("enfant-m", "Oui."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0003_F0001",
        [
            ("narrateur", "Amir tient la sangle du sac."),
            ("papa", "Le sac est prêt."),
            ("enfant-m", "La casserole aussi."),
            ("narrateur", "Il fait semblant de cuire le pain."),
            ("maman", "Tout doux. C'est déjà cuit."),
            ("narrateur", "Amir rit."),
            ("narrateur", "La cuisine est calme."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# pain + jardin
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002",
        [
            ("narrateur", "Amir descend la marche du jardin."),
            ("narrateur", "Le pain reste au fond du sac."),
            ("narrateur", "Le vent est doux sur les joues."),
            ("narrateur", "Un petit chapeau attend sur le banc."),
            ("papa", "Le petit chapeau, dans le sac."),
            ("enfant-m", "Le chapeau."),
            ("narrateur", "Le chapeau est souple."),
            ("narrateur", "Amir le tasse près du pain."),
            ("narrateur", "Une feuille tourne au-dessus du bac."),
            ("papa", "On la laisse au jardin."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0001",
        [
            ("narrateur", "Les cubes sont dans le bac à sable."),
            ("narrateur", "Un cube a un peu de sable."),
            ("narrateur", "Amir le frotte."),
            ("papa", "Le cube propre, dans le sac."),
            ("enfant-m", "Le cube propre."),
            ("narrateur", "Il le met près du pain."),
            ("papa", "Le sable reste au bac."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0001_F0001",
        [
            ("narrateur", "Amir remonte la marche avec le sac."),
            ("enfant-m", "Merci, papa."),
            ("maman", "On joue au cube, une minute."),
            ("narrateur", "Amir pose le cube sur la marche."),
            ("narrateur", "Une feuille reste sur le bac."),
            ("papa", "On rentre."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0002",
        [
            ("narrateur", "Le livre est sous le chapeau, sur le banc."),
            ("narrateur", "Une page tremble au vent."),
            ("maman", "Le livre dans le sac."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Amir le met près du pain."),
            ("narrateur", "Puis le chapeau par-dessus."),
            ("maman", "Le chapeau garde le livre."),
            ("enfant-m", "Oui."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac est un peu lourd."),
            ("enfant-m", "Merci."),
            ("papa", "On rentre avec le sac."),
            ("narrateur", "Amir soulève le chapeau."),
            ("narrateur", "Il touche le livre, juste un peu."),
            ("narrateur", "Le jardin sent la terre mouillée."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0003",
        [
            ("narrateur", "Une assiette de dînette est sur le muret."),
            ("narrateur", "Un caillou rond est posé dessus."),
            ("narrateur", "Amir pose le caillou à côté."),
            ("maman", "L'assiette dans le sac."),
            ("enfant-m", "L'assiette."),
            ("narrateur", "Il la met près du pain."),
            ("maman", "On y mettra le pain, pour de faux."),
            ("enfant-m", "Pour de faux."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0003_F0001",
        [
            ("narrateur", "Amir serre le sac contre lui."),
            ("enfant-m", "Le sac est prêt."),
            ("papa", "Merci, maman."),
            ("narrateur", "Amir sort l'assiette."),
            ("narrateur", "Il y pose le pain un instant."),
            ("narrateur", "Puis tout rentre."),
            ("narrateur", "Le vent est plus calme."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# pain + chambre
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003",
        [
            ("narrateur", "Amir repose le sac sur le tapis rayé."),
            ("narrateur", "Le pain fait un petit bruit de croûte."),
            ("narrateur", "Le volet jaune claque une fois."),
            ("narrateur", "Le doudou attend près de l'oreiller."),
            ("maman", "Le doudou du sac, Amir."),
            ("enfant-m", "Le doudou."),
            ("narrateur", "Le doudou est chaud et un peu plat."),
            ("narrateur", "Amir le glisse près du pain."),
            ("maman", "Il est bien dedans ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Le sac se remplit."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0000",
        [
            ("narrateur", "On peut prendre quoi ?"),
            ("narrateur", "Les cubes, le livre, ou la dînette."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0001",
        [
            ("narrateur", "Les cubes sont près du doudou, sur le tapis."),
            ("narrateur", "Un cube touche la patte du doudou."),
            ("papa", "Les cubes dans le sac."),
            ("enfant-m", "Les cubes."),
            ("narrateur", "Amir les met près du pain et du doudou."),
            ("papa", "La patte est libre."),
            ("enfant-m", "Libre."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0001_F0001",
        [
            ("narrateur", "Amir ferme le sac sur le tapis rayé."),
            ("enfant-m", "On peut jouer maintenant."),
            ("maman", "Oui."),
            ("narrateur", "Il sort un cube."),
            ("narrateur", "Il le pose sur le doudou, pour rire."),
            ("papa", "Le volet jaune est calme."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0002",
        [
            ("narrateur", "Le livre est sous l'oreiller."),
            ("narrateur", "Amir soulève l'oreiller d'une main."),
            ("papa", "Le livre dans le sac."),
            ("enfant-m", "Le livre."),
            ("narrateur", "Il le glisse près du pain."),
            ("papa", "Sous le doudou, tout doux."),
            ("enfant-m", "Tout doux."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0002_F0001",
        [
            ("narrateur", "Le sac attend près de la porte de la chambre."),
            ("enfant-m", "Merci, papa."),
            ("maman", "On lit une page ?"),
            ("narrateur", "Amir ouvre le livre contre le doudou."),
            ("narrateur", "Le tapis n'a plus de cubes."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0003",
        [
            ("narrateur", "La dînette est dans le panier, près du lit."),
            ("narrateur", "Une tasse et une assiette s'entrechoquent."),
            ("maman", "La tasse seulement."),
            ("enfant-m", "La tasse."),
            ("narrateur", "Amir prend la tasse."),
            ("narrateur", "Il la met près du pain."),
            ("maman", "L'assiette reste."),
            ("enfant-m", "Elle reste."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0003_F0001",
        [
            ("narrateur", "Amir s'assoit, le sac sur les genoux."),
            ("papa", "Le sac est prêt."),
            ("enfant-m", "Merci."),
            ("narrateur", "Il sort la tasse."),
            ("narrateur", "Il y glisse un tout petit bout de pain."),
            ("maman", "Pour de faux. Puis on range."),
            ("narrateur", "La chambre sent encore la soupe, un peu."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)


def word_count(s: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9']+", s))


def main() -> None:
    ids_src = [c["chunk_id"] for c in SRC["chunks"]]
    ids_new = [c["chunk_id"] for c in CHUNKS]
    missing = [i for i in ids_src if i not in ids_new]
    extra = [i for i in ids_new if i not in ids_src]
    if missing or extra or len(ids_new) != len(set(ids_new)):
        raise SystemExit(f"ids mismatch missing={missing} extra={extra} dup={len(ids_new)-len(set(ids_new))}")

    long_lines = []
    bravo = 0
    slogan = 0
    lina = 0
    no_fin = []
    for c in CHUNKS:
        if "bravo" in (c["text"] or "").lower():
            bravo += 1
        if "l'adulte a dit" in (c["text"] or "").lower() or "ce que l'adulte" in (c["text"] or "").lower():
            slogan += 1
        if re.search(r"\bLina\b", c["text"] or ""):
            lina += 1
        if c["kind"] == "passage_fin" and "L'histoire est finie." not in c["text"]:
            no_fin.append(c["chunk_id"])
        for line in c["script"].splitlines():
            phrase = line.split("|", 1)[1] if "|" in line else line
            n = word_count(phrase)
            if n > 12:
                long_lines.append((c["chunk_id"], n, phrase))

    by_new = {c["chunk_id"]: c for c in CHUNKS}
    ordered = [by_new[i] for i in ids_src]
    payload = {
        "story_id": "TREE-AUT-001",
        "fil_rouge": (
            "Amir veut aller jouer. Son sac est vide sur le tapis rayé. "
            "Il demande à papa et maman. Il met la pomme, le yaourt ou le pain, "
            "puis ce qu'ils nomment. Quand le sac est fermé, il joue enfin."
        ),
        "title": "Le sac d'Amir sur le tapis rayé",
        "lesson_id": "AUT.AFF.001",
        "age_band": "N1",
        "kind": "ramifiee",
        "characters": "Amir, maman, papa",
        "setting": "dans la chambre",
        "chunks": ordered,
        "proof": {
            "chunks": 86,
            "bravo_chunks": bravo,
            "slogan_adulte": slogan,
            "lina": lina,
            "long_lines_gt12": long_lines,
            "fins_sans_cloture": no_fin,
        },
    }
    out = HERE / "merged.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} n={len(ordered)} bravo={bravo} slogan={slogan} lina={lina}")
    print(f"long>12: {len(long_lines)} fin_manquante={no_fin}")
    if long_lines:
        for cid, n, p in long_lines[:20]:
            print(f"  {n:2} {cid} {p}")


if __name__ == "__main__":
    main()
