# TREE-AUT-035 — relecture éditoriale

- **Titre noyau conservé :** *Le fil d'argent et le radiateur de Nina*
- **Public :** 5–6 ans (N3)
- **Leçon :** AUT.ROU.001 — enchaîner le matin, vécue (manteau, gant, radiateur, puis la cour)
- **Personnages :** Nina, papa, maman
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

## Promesse narrative

Après l'averse, un fil d'argent descend la vitre du vestiaire vers une flaque qui tient un morceau de ciel. Nina veut y courir tout de suite. Elle pousse la porte, manteau ouvert : le gant rouge tombe, les doigts nus ne tiennent plus la poignée. Selon le jeu choisi, la pelle, la rampe ou les chaînes refusent sa main nue. Elle revient au tic du radiateur, accroche, retrouve la paire, réchauffe les paumes. Alors seulement le ballon, le seau ou le doudou cessent de lui échapper, et le préau, la fontaine ou le cartable ferment la matinée. Le fil est toujours sur la vitre.

## Améliorations

- Désir ≠ leçon : Nina veut la flaque et le fil, pas « apprendre à s'habiller ».
- Imprévu concret : gant tombé, poignée, pelle, rampe ou chaîne trop froides.
- Première tentative ratée à l'ouverture, puis une autre dans chaque lieu, puis un raté d'objet (ballon qui file, seau qui bascule, doudou trop près de l'eau ou des chaînes).
- T1/T2/T3 changent l'action, pas seulement le décor.
- Le rangement et l'enchaînement se voient (crochet, paire, paumes sur le métal, boucle clic) ; ils ne se disent pas.
- Papa et maman parlent, questionnent, remercient une fois le gant revenu. Pas de règle récitée.
- Chaque fin paie le fil, le tic, ou la flaque, avec un souvenir unique du chemin.
- Tics « encore / déjà / tout doux / tout calme » écartés. Pas d'escargot COL-015.

## Direction vocale

Chaque chunk a `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration), plus `text_ssml`, `text_xai_tags`, pauses, pitch, volume. `slow` réservé aux choix, à la question et aux fins. Action plus vive.

## Relu

Ouverture, 3 passages T1, 3 questions, 3 confirmations, 9 passages T2, 9 choix T3, 27 résolutions, 27 fins. `chunk_id` / `kind` / graphe inchangés.

## Contrôles

- 86 chunks
- 27 chemins
- 27 fins textuellement distinctes
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` sur les 86
- `check()` N3 ≤ 16
- aucune occurrence de « on va apprendre », « une étape après l'autre », « on va ranger »

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
