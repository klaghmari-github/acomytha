# TREE-AUT-027 — Le manteau bleu de Mila au marché

Réécriture éditoriale F-NAR-019. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Le seuil tient l'ombre ovale du panier. Au loin, la bâche rayée claque. Sur le crochet, un manteau bleu attend : le bouton du bas a une entaille en lune, et fait toc contre le bois. Mila veut une orange avant que le stand plie. Elle court sans le manteau : l'air pique. Elle tire trop fort, le bouton accroche. Cuisine, jardin ou chambre, le bleu glisse. Elle le reprend. Cubes, livre ou dînette : une ombre bleue ment. Matin, sieste ou soir, sous la bâche, elle refuse de foncer. Le toc paie le début. L'orange rentre. Le manteau garde une trace.

## Arc dramatique

- Monde : maison près du marché, crochet de bois, bâche rayée, oranges.
- Désir : rapporter une orange avant que la bâche se plie.
- Objet : manteau bleu (bouton à lune, toc), plus cubes / livre / dînette.
- Urgence douce : le stand va plier.
- Imprévu 1 : partir sans manteau, tirer, le bouton accroche ; le bleu glisse.
- Cue : lever le bouton, sans tirer. Un merci vécu.
- Imprévu 2 (plus rusé) : une ombre bleue, un sac, un pli de bâche mentent.
- Résolution : refuser de foncer, écouter le toc, retrouver l'entaille.
- Retour : toc au crochet, orange, 27 traces distinctes.

## Corrections éditoriales

- Le premier choix n'enlève pas le manteau : il vient en cuisine, au jardin, en chambre.
- Revers allongé : froid, glissade, ombre fausse, bâche, geste lent.
- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.AFF.002 vécue (reprendre le manteau), jamais dite.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Mila, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience au départ, petit découragement quand le manteau résiste ou disparaît, fierté calme quand Mila écoute le toc. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 599 à 625 mots par chemin, moyenne 611
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N2 ≤ 15 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
