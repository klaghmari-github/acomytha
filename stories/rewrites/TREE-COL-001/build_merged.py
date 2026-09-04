#!/usr/bin/env python3
"""F-NAR-010…015 — texte TREE-COL-001 (archive). One-shot."""

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
        "length_scale_piper": src.get("length_scale_piper") or 1.22,
        "rate_label": src.get("rate_label") or "slow",
        "pause_after_ms": src.get("pause_after_ms"),
    }


CHUNKS: list[dict] = []

# Désir : donner des pommes à Mila. Leçon greffée : bonjour / s'il te plaît / merci, vécus.
CHUNKS.append(
    pack(
        "CHK_T0000_P0000",
        [
            ("narrateur", "Une goutte glisse le long de la casserole."),
            ("narrateur", "Ça sent la pomme, toute douce."),
            ("narrateur", "Le torchon rayé pend près de l'évier."),
            ("narrateur", "Dehors, le marché parle tout bas."),
            ("narrateur", "Un rond de soleil pose sur le carrelage."),
            ("narrateur", "Les chaussons de Raphaël attendent sous la table."),
            ("papa", "La casserole chante un peu, Raphaël."),
            ("maman", "Tu as vu le torchon ?"),
            ("enfant-m", "Il est rouge et blanc."),
            ("narrateur", "Papa pose des rondelles dans un bol jaune."),
            ("narrateur", "Le bois de la planche est lisse, un peu humide."),
            ("narrateur", "En ce moment, Raphaël tient une cuillère en bois."),
            ("enfant-m", "Je veux donner des pommes à Mila."),
            ("maman", "Elle arrive tout à l'heure."),
            ("papa", "Tu prends un jouet, en attendant ?"),
            ("narrateur", "Le bol jaune attend au milieu."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0000",
        [
            ("narrateur", "Qu'est-ce que Raphaël prend ?"),
            ("narrateur", "Le train, le bus, ou la voiture."),
        ],
    )
)

# --- train -----------------------------------------------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0001",
        [
            ("narrateur", "Raphaël prend le train en bois."),
            ("narrateur", "Les roues font un petit clic sur le carrelage."),
            ("narrateur", "La porte de la cuisine s'ouvre."),
            ("narrateur", "Mila entre, les joues roses."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour, Raphaël."),
            ("narrateur", "Le train s'arrête près de ses pieds."),
            ("papa", "Tu veux une rondelle, Mila ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Papa tend une pomme, toute lisse."),
            ("enfant-f", "Merci."),
            ("enfant-m", "Moi aussi ?"),
            ("papa", "Demande."),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Une rondelle froide dans sa main."),
            ("enfant-m", "Merci, papa."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0001_Q0001", [("narrateur", "Mila arrive. Raphaël dit quoi ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_C0001",
        [
            ("narrateur", "Raphaël a dit bonjour."),
            ("narrateur", "Mila a une rondelle."),
            ("narrateur", "Le train attend près du bol jaune."),
            ("enfant-m", "On joue encore ?"),
            ("maman", "Oui. On s'installe."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0000",
        [
            ("narrateur", "On va où, dans la cuisine ?"),
            ("narrateur", "La table, la fenêtre, ou le tabouret."),
        ],
    )
)

def time_q(cid: str) -> None:
    CHUNKS.append(
        pack(
            cid,
            [
                ("narrateur", "C'est quel moment ?"),
                ("narrateur", "Le matin, après la sieste, ou le soir."),
            ],
        )
    )


# train + table
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001",
        [
            ("narrateur", "Raphaël pose le train près de la table."),
            ("narrateur", "Le bol jaune est au milieu."),
            ("narrateur", "Mila tire une chaise, tout doux."),
            ("maman", "Une assiette, Raphaël ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "L'assiette est ronde, un peu froide."),
            ("enfant-m", "Merci, maman."),
            ("narrateur", "Il pose une rondelle dans l'assiette de Mila."),
            ("enfant-f", "Merci, Raphaël."),
        ],
    )
)
time_q("CHK_T0001_P0001_T0002_P0001_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Le soleil touche une roue du train."),
            ("narrateur", "Ça sent le lait et la pomme."),
            ("papa", "Encore une rondelle, Mila ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "La pomme est froide, un peu sucrée."),
            ("enfant-f", "Merci, papa."),
            ("narrateur", "Raphaël fait le tour du bol avec le train."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0001_F0001",
        [
            ("narrateur", "Le train s'arrête contre le bol jaune."),
            ("enfant-m", "Terminus, les pommes."),
            ("enfant-f", "Merci pour le voyage."),
            ("maman", "Bonne journée, vous deux."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "La casserole est encore tiède."),
            ("narrateur", "Mila bâille, tout petit."),
            ("papa", "On joue tout doux."),
            ("narrateur", "Raphaël pousse le train sans le bruit des roues."),
            ("enfant-f", "Encore une rondelle ?"),
            ("enfant-m", "S'il te plaît, papa."),
            ("narrateur", "Papa en glisse une."),
            ("enfant-m", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0002_F0001",
        [
            ("narrateur", "Le train dort contre l'assiette."),
            ("enfant-m", "Chut. Il fait la sieste aussi."),
            ("maman", "Vous avez bien partagé."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "Une lampe éclaire la table."),
            ("narrateur", "Le marché, dehors, s'est tu."),
            ("maman", "On range bientôt."),
            ("narrateur", "Raphaël gare le train sous sa chaise."),
            ("enfant-f", "Encore une pomme ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "La dernière rondelle brille."),
            ("enfant-f", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0001_T0003_P0003_F0001",
        [
            ("narrateur", "Le bol jaune est vide."),
            ("papa", "Le train est au garage."),
            ("enfant-m", "À demain, Mila."),
            ("enfant-f", "À demain."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# train + fenêtre
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002",
        [
            ("narrateur", "Raphaël va près de la fenêtre, avec le train."),
            ("narrateur", "La vitre est un peu floue."),
            ("narrateur", "Mila trace un petit rond du doigt."),
            ("papa", "Le torchon, pour la vitre ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Le torchon est doux, un peu épais."),
            ("enfant-m", "Merci, papa."),
            ("narrateur", "Il essuie un rond. Le marché apparaît."),
            ("enfant-f", "Je vois le stand des pommes."),
        ],
    )
)
time_q("CHK_T0001_P0001_T0002_P0002_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Le soleil chauffe la vitre."),
            ("narrateur", "Raphaël pose le train sur le rebord."),
            ("maman", "Une rondelle, en regardant ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Mila mange, les yeux dehors."),
            ("enfant-f", "Merci."),
            ("enfant-m", "Mon train va au marché."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0001_F0001",
        [
            ("narrateur", "Un oiseau passe derrière la vitre."),
            ("enfant-m", "Arrêt marché."),
            ("papa", "Vous avez bien regardé ensemble."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "La lumière est douce, un peu jaune."),
            ("narrateur", "Raphaël pousse le train le long du rebord."),
            ("enfant-f", "Il fait moins de bruit."),
            ("papa", "Une rondelle calme ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0002_F0001",
        [
            ("narrateur", "Le train s'arrête contre le bois de la fenêtre."),
            ("enfant-f", "Il dort au soleil."),
            ("maman", "On reste encore un peu."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "La vitre devient sombre."),
            ("narrateur", "Des lampes s'allument au marché."),
            ("maman", "On dit au revoir à la rue."),
            ("narrateur", "Raphaël descend le train du rebord."),
            ("enfant-f", "Encore une pomme ?"),
            ("papa", "S'il te plaît, on demande."),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0002_T0003_P0003_F0001",
        [
            ("narrateur", "Le train rentre dans la gare, sous la table."),
            ("enfant-m", "Les lampes, c'est fini."),
            ("papa", "À demain, le marché."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# train + tabouret
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003",
        [
            ("narrateur", "Raphaël glisse le train près du tabouret."),
            ("narrateur", "Le tabouret est bas, en bois clair."),
            ("narrateur", "Mila s'assoit, les pieds qui balancent."),
            ("enfant-m", "Je peux le tabouret, après ?"),
            ("enfant-f", "S'il te plaît, tu attends."),
            ("enfant-m", "D'accord."),
            ("narrateur", "Il pose le bol jaune sur les genoux de Mila."),
            ("enfant-f", "Merci."),
            ("narrateur", "Le tabouret fait un tout petit craquement."),
        ],
    )
)
time_q("CHK_T0001_P0001_T0002_P0003_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Le soleil touche les pieds de Mila."),
            ("narrateur", "Raphaël fait le tour du tabouret avec le train."),
            ("papa", "Une rondelle, du haut du tabouret ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
            ("enfant-m", "Mon tour ?"),
            ("enfant-f", "Oui. Merci d'avoir attendu."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0001_F0001",
        [
            ("narrateur", "Raphaël s'assoit. Le train monte avec lui."),
            ("maman", "Vous avez attendu chacun votre tour."),
            ("enfant-m", "Les pommes aussi."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "Mila pose la tête un instant."),
            ("narrateur", "Raphaël arrête le train contre un pied du tabouret."),
            ("maman", "Tout doux."),
            ("enfant-m", "Une rondelle, s'il te plaît."),
            ("narrateur", "Papa en pose deux, tout près."),
            ("enfant-m", "Merci. Une pour Mila."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0002_F0001",
        [
            ("narrateur", "Mila ouvre les yeux."),
            ("enfant-f", "Merci. Elle était pour moi."),
            ("papa", "Le train a attendu aussi."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "L'ombre du tabouret s'allonge."),
            ("narrateur", "Raphaël gare le train dessous."),
            ("enfant-f", "Je descends ?"),
            ("enfant-m", "Oui. Merci, Mila."),
            ("maman", "Une dernière rondelle ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0001_T0002_P0003_T0003_P0003_F0001",
        [
            ("narrateur", "Le tabouret est vide."),
            ("narrateur", "Le train dort en dessous."),
            ("papa", "Vous avez partagé le siège et les pommes."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# --- bus -------------------------------------------------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0002",
        [
            ("narrateur", "Raphaël prend le bus rouge."),
            ("narrateur", "Dehors, un vrai bus passe, tout bas."),
            ("narrateur", "Mila pousse la porte de la cuisine."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour."),
            ("narrateur", "Raphaël veut essuyer une miette."),
            ("enfant-m", "Le torchon, s'il te plaît."),
            ("maman", "Voilà le torchon."),
            ("enfant-m", "Merci, maman."),
            ("narrateur", "Il essuie le rebord du bol."),
            ("papa", "Tu veux une rondelle ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0002_Q0001", [("narrateur", "Raphaël veut le torchon. Que dit-il ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_C0001",
        [
            ("narrateur", "Raphaël a dit s'il te plaît."),
            ("narrateur", "Le torchon rayé est dans sa main."),
            ("narrateur", "Le bus rouge attend près du tabouret."),
            ("enfant-f", "On monte ?"),
            ("maman", "On s'installe d'abord."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0000",
        [
            ("narrateur", "On va où, dans la cuisine ?"),
            ("narrateur", "La table, la fenêtre, ou le tabouret."),
        ],
    )
)

# bus + table
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001",
        [
            ("narrateur", "Raphaël pose le bus rouge près de la table."),
            ("narrateur", "Le bol jaune est au milieu."),
            ("narrateur", "Mila tire une chaise."),
            ("enfant-m", "Arrêt table."),
            ("maman", "Deux assiettes ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Les assiettes font un petit toc."),
            ("enfant-m", "Merci."),
            ("narrateur", "Il glisse une rondelle vers Mila."),
            ("enfant-f", "Merci. Ticket pomme."),
        ],
    )
)
time_q("CHK_T0001_P0002_T0002_P0001_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Dehors, le vrai bus klaxonne, tout loin."),
            ("narrateur", "Raphaël ouvre la porte du bus rouge."),
            ("papa", "On charge les pommes ?"),
            ("enfant-m", "S'il te plaît, une pour Mila."),
            ("narrateur", "Papa pose deux rondelles sur les sièges."),
            ("enfant-f", "Merci. On part."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0001_F0001",
        [
            ("narrateur", "Le bus fait le tour de la table."),
            ("enfant-m", "Prochain arrêt : le bol."),
            ("maman", "Vous avez bien chargé."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "Le bus rouge avance tout lentement."),
            ("enfant-f", "Les voyageurs ont sommeil."),
            ("maman", "Une rondelle calme ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
            ("narrateur", "Raphaël ferme la porte du bus, tout doux."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0002_F0001",
        [
            ("narrateur", "Le bus reste collé à l'assiette."),
            ("enfant-m", "Terminus sieste."),
            ("papa", "On ne réveille pas les pommes."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "La table a une petite ombre."),
            ("narrateur", "Raphaël range le bus sous une serviette."),
            ("enfant-f", "Le dépôt."),
            ("papa", "Dernière rondelle ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci. Pour Mila aussi."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0001_T0003_P0003_F0001",
        [
            ("narrateur", "Le bol est vide. Le bus est au dépôt."),
            ("maman", "Bonne soirée, les voyageurs."),
            ("enfant-f", "Merci pour le trajet."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# bus + fenêtre
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002",
        [
            ("narrateur", "Raphaël va près de la fenêtre, avec le bus."),
            ("narrateur", "Un vrai bus passe dans la rue."),
            ("narrateur", "Mila colle son nez à la vitre."),
            ("enfant-m", "Le torchon, s'il te plaît."),
            ("papa", "Pour voir le bus ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Il essuie. Le bus rouge de vrai apparaît."),
            ("enfant-m", "Merci, papa."),
            ("enfant-f", "Le nôtre est plus petit."),
        ],
    )
)
time_q("CHK_T0001_P0002_T0002_P0002_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Le vrai bus s'arrête au coin."),
            ("narrateur", "Raphaël pose le petit bus sur le rebord."),
            ("maman", "Rondelle du chauffeur ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci. Une pour Mila."),
            ("enfant-f", "Merci. On suit le grand."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0001_F0001",
        [
            ("narrateur", "Le vrai bus repart. Le petit reste."),
            ("enfant-m", "On garde les pommes ici."),
            ("papa", "Bon trajet, vous deux."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "La rue est plus calme."),
            ("narrateur", "Raphaël fait glisser le bus le long du bois."),
            ("enfant-f", "Pas de klaxon."),
            ("papa", "Une pomme, tout bas ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0002_F0001",
        [
            ("narrateur", "Le petit bus s'endort contre la vitre."),
            ("maman", "Le grand reviendra plus tard."),
            ("enfant-m", "On l'attendra."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "Les feux du vrai bus passent, tout rouge."),
            ("narrateur", "Raphaël descend le petit bus du rebord."),
            ("maman", "On rentre au dépôt."),
            ("enfant-m", "Une rondelle, s'il te plaît."),
            ("enfant-m", "Merci."),
            ("enfant-f", "Bonne nuit, le bus."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0002_T0003_P0003_F0001",
        [
            ("narrateur", "La vitre est noire, maintenant."),
            ("papa", "Le marché est fermé."),
            ("enfant-m", "Notre bus aussi."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# bus + tabouret
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003",
        [
            ("narrateur", "Raphaël glisse le bus près du tabouret."),
            ("narrateur", "Mila s'assoit. Les pieds balancent."),
            ("enfant-m", "Arrêt tabouret."),
            ("enfant-f", "Je descends ?"),
            ("enfant-m", "Tu peux rester."),
            ("maman", "Le bol, plus haut ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "Maman pose le bol sur le tabouret, à côté de Mila."),
            ("enfant-m", "Merci."),
        ],
    )
)
time_q("CHK_T0001_P0002_T0002_P0003_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Le soleil fait un rectangle sur le bois."),
            ("narrateur", "Raphaël fait monter le bus sur le rectangle."),
            ("papa", "Tickets pommes ?"),
            ("enfant-f", "S'il te plaît."),
            ("narrateur", "Deux rondelles sur les genoux de Mila."),
            ("enfant-f", "Merci. Une pour le chauffeur."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0001_F0001",
        [
            ("narrateur", "Raphaël croque. Mila croque."),
            ("enfant-m", "Prochain arrêt : demain."),
            ("maman", "Vous avez bien attendu le bol."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "Mila balance moins les pieds."),
            ("narrateur", "Raphaël gare le bus contre un pied."),
            ("papa", "On charge tout doux."),
            ("enfant-m", "Une rondelle, s'il te plaît."),
            ("enfant-m", "Merci. Pour Mila."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0002_F0001",
        [
            ("narrateur", "Le bus ne roule plus."),
            ("enfant-f", "Merci. J'avais sommeil."),
            ("papa", "Le tabouret a bien tenu."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "Raphaël range le bus sous le tabouret."),
            ("enfant-f", "Le dépôt est en bas."),
            ("maman", "On descend du siège ?"),
            ("enfant-f", "Oui. Merci, tabouret."),
            ("papa", "Dernière pomme ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0002_T0002_P0003_T0003_P0003_F0001",
        [
            ("narrateur", "Mila pose les pieds par terre."),
            ("enfant-m", "Le bus dort en dessous."),
            ("maman", "Vous avez bien partagé le haut et le bas."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# --- voiture ---------------------------------------------------------------
CHUNKS.append(
    pack(
        "CHK_T0001_P0003",
        [
            ("narrateur", "Raphaël prend la petite voiture."),
            ("narrateur", "Elle est lisse, un peu froide."),
            ("narrateur", "Dehors, une portière claque, tout loin."),
            ("narrateur", "Mila arrive. Son manteau sent la pluie."),
            ("enfant-m", "Bonjour, Mila."),
            ("enfant-f", "Bonjour, Raphaël."),
            ("maman", "Donne-moi ton manteau ?"),
            ("enfant-f", "S'il te plaît, tu peux le prendre."),
            ("narrateur", "Maman accroche le manteau."),
            ("enfant-f", "Merci."),
            ("papa", "Une rondelle, Raphaël ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "La rondelle est froide et douce."),
            ("enfant-m", "Merci, papa."),
        ],
    )
)
CHUNKS.append(pack("CHK_T0001_P0003_Q0001", [("narrateur", "Papa donne une rondelle. Que dit Raphaël ?")]))
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_C0001",
        [
            ("narrateur", "Raphaël a dit merci."),
            ("narrateur", "La petite voiture brille près du bol."),
            ("narrateur", "Le manteau de Mila sèche un peu."),
            ("enfant-m", "On roule ?"),
            ("papa", "On s'installe."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0000",
        [
            ("narrateur", "On va où, dans la cuisine ?"),
            ("narrateur", "La table, la fenêtre, ou le tabouret."),
        ],
    )
)

# voiture + table
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001",
        [
            ("narrateur", "Raphaël pose la petite voiture près de la table."),
            ("narrateur", "Une goutte du manteau tombe. Toc."),
            ("narrateur", "Mila tire une chaise."),
            ("maman", "Une assiette, pour ne pas mouiller ?"),
            ("enfant-m", "S'il te plaît."),
            ("narrateur", "L'assiette arrive, ronde."),
            ("enfant-m", "Merci."),
            ("narrateur", "Il y pose une rondelle pour Mila."),
            ("enfant-f", "Merci. Ma voiture à moi, c'est la chaise."),
        ],
    )
)
time_q("CHK_T0001_P0003_T0002_P0001_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "La goutte a déjà séché."),
            ("narrateur", "Raphaël fait le tour des assiettes avec la voiture."),
            ("papa", "Encore une pomme, chauffeur ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci. Mila aussi."),
            ("enfant-f", "Merci. On va au marché, pour de faux."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0001_F0001",
        [
            ("narrateur", "La voiture se gare contre le bol jaune."),
            ("enfant-m", "Parking pommes."),
            ("maman", "Vous avez bien servi."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "La voiture avance entre les miettes, tout lent."),
            ("enfant-f", "Pas trop vite. J'ai encore sommeil."),
            ("maman", "Une rondelle ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
            ("narrateur", "Raphaël arrête la voiture près de sa main."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0002_F0001",
        [
            ("narrateur", "La voiture fait un tout petit phare : le soleil."),
            ("papa", "On reste au parking."),
            ("enfant-m", "Les pommes aussi."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "Raphaël gare la voiture sous la table."),
            ("maman", "On reprend le manteau bientôt."),
            ("enfant-f", "Encore une pomme ?"),
            ("enfant-m", "S'il te plaît, papa."),
            ("narrateur", "La dernière rondelle."),
            ("enfant-f", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0001_T0003_P0003_F0001",
        [
            ("narrateur", "Mila enfile son manteau. Il est presque sec."),
            ("enfant-m", "À demain."),
            ("enfant-f", "Merci pour les pommes."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# voiture + fenêtre
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002",
        [
            ("narrateur", "Raphaël va près de la fenêtre, avec la voiture."),
            ("narrateur", "La vitre a encore un peu de buée."),
            ("narrateur", "Mila dessine une route du doigt."),
            ("enfant-m", "Le torchon, s'il te plaît."),
            ("papa", "Pour la route ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "La buée part. La rue apparaît."),
            ("enfant-m", "Merci, papa."),
            ("enfant-f", "Ta voiture peut y aller."),
        ],
    )
)
time_q("CHK_T0001_P0003_T0002_P0002_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Une vraie voiture passe, tout loin."),
            ("narrateur", "Raphaël suit la route sur la vitre."),
            ("maman", "Rondelle du voyage ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
            ("enfant-m", "On va au marché des pommes."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0001_F0001",
        [
            ("narrateur", "La petite voiture s'arrête au bas de la vitre."),
            ("papa", "Vous êtes arrivés."),
            ("enfant-m", "Les pommes aussi."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "La rue est calme."),
            ("narrateur", "Raphaël pose la voiture sur le rebord, sans la pousser."),
            ("papa", "Une pomme, sans bouger ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci. Pour Mila."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0002_F0001",
        [
            ("narrateur", "La voiture reste. Mila reste."),
            ("enfant-f", "Merci. On regarde seulement."),
            ("maman", "C'est bien, parfois."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "Des phares passent sur la vitre."),
            ("narrateur", "Raphaël descend la voiture."),
            ("enfant-f", "On rentre."),
            ("maman", "Une pomme avant le manteau ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0002_T0003_P0003_F0001",
        [
            ("narrateur", "Mila reprend son manteau."),
            ("enfant-m", "À demain, la route."),
            ("papa", "La voiture est au garage, sous la fenêtre."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)

# voiture + tabouret
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003",
        [
            ("narrateur", "Raphaël glisse la voiture près du tabouret."),
            ("narrateur", "Mila s'assoit. Les pieds balancent."),
            ("enfant-m", "Je monte la voiture ?"),
            ("enfant-f", "S'il te plaît, tout doux."),
            ("narrateur", "Il pose la voiture sur le bois, près d'elle."),
            ("enfant-m", "Merci, Mila."),
            ("maman", "Le bol, à votre hauteur ?"),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci."),
        ],
    )
)
time_q("CHK_T0001_P0003_T0002_P0003_T0003_P0000")
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0001",
        [
            ("narrateur", "C'est le matin."),
            ("narrateur", "Le soleil fait un parking sur le tabouret."),
            ("narrateur", "Raphaël gare la voiture dans le carré de lumière."),
            ("papa", "Pommes du parking ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci. Une pour Raphaël."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0001_F0001",
        [
            ("narrateur", "Ils croquent, les pieds en l'air."),
            ("enfant-m", "Belle place."),
            ("maman", "Vous avez bien demandé le bol."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0002",
        [
            ("narrateur", "C'est après la sieste."),
            ("narrateur", "La voiture ne roule plus. Elle attend."),
            ("enfant-f", "Moi aussi, j'attends."),
            ("papa", "Une rondelle, alors."),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Merci. On partage."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0002_F0001",
        [
            ("narrateur", "Deux rondelles. Deux sourires."),
            ("maman", "Le tabouret a tenu le goûter."),
            ("enfant-f", "Merci, tabouret."),
            ("narrateur", "L'histoire est finie."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0003",
        [
            ("narrateur", "C'est le soir."),
            ("narrateur", "Raphaël descend la voiture du tabouret."),
            ("enfant-f", "Je descends aussi."),
            ("enfant-m", "Merci d'avoir gardé la place."),
            ("maman", "Manteau ?"),
            ("enfant-f", "S'il te plaît."),
            ("enfant-f", "Merci."),
            ("papa", "Et une pomme pour la route."),
        ],
    )
)
CHUNKS.append(
    pack(
        "CHK_T0001_P0003_T0002_P0003_T0003_P0003_F0001",
        [
            ("narrateur", "Mila enfile son manteau. Il sent encore un peu la pluie."),
            ("enfant-m", "À demain."),
            ("enfant-f", "Merci pour les pommes et la voiture."),
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
        raise SystemExit(f"ids mismatch missing={missing} extra={extra} dups={len(ids_new)-len(set(ids_new))}")

    long_lines = []
    bravo = slogan = lina = sami = tom = lea = 0
    no_fin = []
    for c in CHUNKS:
        t = c["text"] or ""
        tl = t.lower()
        if "bravo" in tl:
            bravo += 1
        if "les trois mots" in tl:
            slogan += 1
        if re.search(r"\bLina\b", t):
            lina += 1
        if re.search(r"\bSami\b", t):
            sami += 1
        if re.search(r"\bTom\b", t):
            tom += 1
        if re.search(r"\bLéa\b", t):
            lea += 1
        if c["kind"] == "passage_fin" and "L'histoire est finie." not in t:
            no_fin.append(c["chunk_id"])
        for line in c["script"].splitlines():
            phrase = line.split("|", 1)[1] if "|" in line else line
            n = word_count(phrase)
            if n > 16:
                long_lines.append((c["chunk_id"], n, phrase))

    by_new = {c["chunk_id"]: c for c in CHUNKS}
    ordered = [by_new[i] for i in ids_src]
    payload = {
        "story_id": "TREE-COL-001",
        "fil_rouge": (
            "Raphaël veut donner des pommes à Mila. La casserole chante. "
            "Il prend un train, un bus ou une voiture. Ils s'installent. "
            "Il dit bonjour, s'il te plaît, merci quand il en a besoin. "
            "Les pommes sont partagées."
        ),
        "title": "La casserole et les pommes de Raphaël",
        "lesson_id": "COL.POL.001",
        "age_band": "N2",
        "kind": "ramifiee",
        "characters": "Raphaël, Mila, maman, papa",
        "setting": "dans la cuisine",
        "chunks": ordered,
        "proof": {
            "chunks": 86,
            "bravo_chunks": bravo,
            "slogan_trois_mots": slogan,
            "lina": lina,
            "sami": sami,
            "tom": tom,
            "lea": lea,
            "long_lines_gt16": long_lines,
            "fins_sans_cloture": no_fin,
        },
    }
    out = HERE / "merged.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} n={len(ordered)} bravo={bravo} slogan={slogan} lina={lina} sami={sami} tom={tom} lea={lea}")
    print(f"long>16: {len(long_lines)} fin_manquante={no_fin}")
    for cid, n, p in long_lines[:15]:
        print(f"  {n:2} {cid} {p}")


if __name__ == "__main__":
    main()
