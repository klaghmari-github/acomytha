# TREE-COL-032 — Le presse-agrumes de Nina

- **Public :** N3, 5–6 ans, lecture interactive familiale
- **Leçon :** COL.POL.001 — demander avec attention et respect (implicite) ; tours de parole vécus
- **Personnages :** Nina, Aniss, papa, maman
- **Lieu :** maison sous la pluie, cuisine, seuil de l'étendoir, chambre
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Un jour de pluie, Aniss arrive bottes mouillées. Nina veut remplir le pichet avec le presse-agrumes **maintenant**. Aniss veut presser l'orange à deux mains. Ils parlent en même temps : le jus gicle, un croissant de zeste s'enfonce sous la vis. Cuisine (table collante), jardin (seuil de l'étendoir) ou chambre (plateau) changent l'obstacle. Cubes, livre ou dînette changent la manière de prendre son tour. Matin, sieste ou soir paient l'indice du début. La demande, après l'écoute, ouvre la manivelle.

## Vécu

Nina veut tourner. Aniss veut presser. Première tentative : ils tirent ensemble, personne n'entend, le zeste coince. Envies de couper, retenue, écoute réelle, plaisir d'être entendu. Papa et maman s'accroupissent, conversationnels. Le croissant de zeste, vu à l'ouverture, revient au climax. 27 fins : le presse-agrumes porte une trace unique.

## Améliorations

- P1 F-NAR-019 / example4 v2 : ouverture par les bottes mouillées, pas le gabarit.
- Indice unique : croissant de zeste sous la vis, payé à chaque climax.
- Deux enfants, deux envies. Première idée échoue. 2e ruse plus maline.
- T1/T2/T3 changent l'action, pas seulement le décor. Presse-agrumes conservé partout.
- Refrains Bonjour / s'il te plaît / merci récités, Bravo bon travail, l'histoire est finie : retirés.
- Tics encore / déjà / tout doux / tout calme : retirés.
- Revers allongé : T3 et fins plus incarnés, souvenir distinct.
- Un merci vécu. TTS par fonction (opening/choice/clue/confirm/action/obstacle/resolution/ending).
- Chemins 733–765 mots (moyenne 749).
- `check()` OK. Pas d'apply. Pas d'audio.

## Direction vocale

Chaque segment a un `notes` : arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration. `slow` réservé aux choix, indices et fins. Action plus vive. Fins : pitch bas, volume doux, pause longue.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins distinctes, 27 climats T3 distincts
- `text` = `script` collé, N3 ≤ 16 mots/phrase
- `text_ssml` et `text_xai_tags` enrichis
- graphe `option_*_next` / `default_next` / `kind` inchangés

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
