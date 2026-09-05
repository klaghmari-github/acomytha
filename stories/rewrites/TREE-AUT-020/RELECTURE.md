# TREE-AUT-020 — Le chat à la fenêtre d'Amir

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types et labels T1/T2/T3 inchangés. Pas d'audio. Pas d'apply. Pas de git.

## Promesse narrative

Près de la fenêtre, un tic minuscule cherche son maître. Un coussin rayé (poc) dort sur le rebord chaud. Un **anneau de pollen** orange, collé côté maison, marque le verre : indice unique, payé au climax. Amir veut rejoindre le chat avant qu'il parte. Il ouvre trop vite : le chat saute, le sourire disparaît. Au jardin des trois coins (bac, toboggan, balançoires — coins, pas jouets qu'on enlève), il jette le coussin. Première idée ratée. Il **reprend** le coussin, sans courir. Ballon, seau ou doudou n'appellent pas le chat, qui file vers la porte. Seconde ruse. Amir refuse de foncer. Manteau, chaussures ou sac portent le même anneau. Il pose un nid sur le rebord. Le chat revient — le dénouement a failli ne pas arriver. AUT.AFF.003 vécue (reprendre ses affaires), jamais dite.

## Améliorations appliquées

- Ouverture par le son (tic) puis l'objet, pas le gabarit v2.
- Indice unique : anneau de pollen (pas marque fine / ombre-flèche / tache).
- Corps : sourire qui part, poitrine, adulte accroupi.
- Deuxième imprévu plus rusé ; l'enfant refuse de foncer.
- 27 fins et 27 dernières images distinctes.
- T1 ne retire pas l'équipement. Un seul enfant (Amir).
- Un merci (bac) et un bravo vécu (toboggan), pas un refrain.
- Pas de « encore / déjà / tout doux », pas merle, pas miel.

## Direction vocale

TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc. `slow` réservé aux choix, à l'indice et aux fins.

## Contrôles

- 86 chunks
- 27 chemins, 676 à 697 mots, moyenne 686
- 7226 mots au total (tous nœuds)
- 27 fins et 27 dernières images distinctes
- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés
- N1 ≤ 10 mots/phrase. `check()` OK.

## Relu

P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Question liée à la scène (reprendre). Impatience, découragement, fierté calme.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
