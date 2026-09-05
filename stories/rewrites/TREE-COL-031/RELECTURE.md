# TREE-COL-031 — Les moufles et le bateau en papier

- **Public :** N3, 5–6 ans, lecture interactive familiale
- **Leçon :** COL.ECO.002 — écouter et prendre son tour de parole (implicite)
- **Personnages :** Victorino, papa, maman
- **Lieu :** petite maison du village, salon et cuisine, matin de pluie
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Sous la pluie, les moufles bleues de Victorino sèchent sur le radiateur. Il a plié un bateau en papier et veut le faire partir tout de suite, avant que la voile ne se gorge. Papa et maman parlent des manteaux : sa première phrase se perd. Une goutte tombe d'une moufle, pile sur la voile. Pour réussir le voyage, il faut s'écouter. Le bassin sur le tapis, le plat sur la table ou le bol à la fenêtre changent le danger. Un livre, un rythme de pluie ou un trait bleu préparent la voile. Le doudou, le camion ou le gobelet décident le vrai départ. Le soir, les moufles sont chaudes et le bateau a une place unique.

## Vécu

Victorino veut lancer son bateau **maintenant**. Il crie trop tôt. Personne n'entend. La voile s'assombrit. Il se tait, touche un coude ou attend le loquet, puis on l'écoute. Chaque choix change l'obstacle, la préparation et le climax. La leçon se voit : parler dans les mots des autres perd le bateau ; attendre la fin de la phrase le sauve.

## Améliorations

- Classe scolaire retirée : maison sous la pluie, radiateur, gouttière, manteaux, orange.
- Première tentative ratée (cri perdu), puis une autre action.
- T1/T2/T3 changent l'enquête, pas seulement le décor.
- T3 Léa/Tom/Sami → le doudou, le camion, le gobelet.
- Refrains « on lève la main / on peut attendre / puis on parle / Bravo bon travail / l'histoire est finie » retirés.
- Un merci vécu, lié au geste (attendre la phrase, reculer les roues, laisser finir le trait).
- 27 fins textuellement distinctes : moufles sèches + place unique du bateau.
- TTS par fonction (opening / choice / clue / confirm / action / obstacle / resolution / ending).

## Direction vocale

Chaque segment a un `notes` : arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration. `slow` réservé aux choix, indices et fins. Action plus vive. Fins : pitch bas, volume doux, pause longue.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins distinctes, 27 climats T3 distincts, 9 T2 distincts
- 630 à 690 mots par chemin (moyenne 654)
- `text` = `script` collé, N3 ≤ 16 mots/phrase
- `text_ssml` et `text_xai_tags` enrichis sur les 86 chunks
- graphe `option_*_next` / `default_next` / `kind` inchangés
- `check()` OK

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
