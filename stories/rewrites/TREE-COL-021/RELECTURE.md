# TREE-COL-021 — La flaque et le ciré de Victorino

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

- **Public :** 3–4 ans (N1), écoute familiale
- **Leçon :** COL.ECO.002 — écouter et prendre son tour de parole (vécue, jamais dite)
- **Personnages :** Victorino, papa, maman
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

## Vécu

Après la pluie, une flaque tient le ciel sous le portail. Le ciré jaune goutte au crochet. Victorino veut y aller tout de suite. Il crie pendant que papa et maman parlent du cacao : personne n'entend. Il ferme la bouche, il attend, puis on l'écoute. Le ciré, les bottes ou le bateau lancent la sortie. La flaque du portail, la gouttière ou le bac changent l'obstacle. Une feuille, un caillou ou la goutte sauvent le petit bateau. À la maison, chacun l'écoute jusqu'au bout.

## Promesse narrative

Le désir n'est pas la leçon : Victorino veut la flaque (et son ciel), pas « apprendre à attendre ». La première idée échoue (crier pendant que les tasses parlent). Un choix change l'action, pas seulement le décor. La fin paie le début : le ciré, les bottes ou le bateau ; la flaque, la gouttière ou le bac ; et la parole qui a enfin une place.

## Vu et corrigé

- Monde d'abord (portail, ciré, goutte, cacao, merle), puis « en ce moment ».
- Première idée échoue ; il touche le coude / pose l'objet / attend que papa finisse.
- Nuance vécue : au bac, il n'attend pas (l'arrosoir menace le bateau).
- Au portail et à la gouttière, deux voix en même temps : une voix, puis l'autre.
- Questions de compréhension (goutte, chaussette, bateau), pas un quiz de règle.
- 27 fins textuellement distinctes ; chaque chemin ramène un détail unique.
- Refrains scolaires retirés : « On lève la main », « Puis on parle », « Bravo / bon travail », « l'histoire est finie », « tout doux / encore / déjà ».
- Un merci vécu quand on l'entend enfin. Papa et maman parlent. Une question d'adulte.
- TTS par fonction (installation, choix, indice, action, obstacle, résolution, retour) : `notes`, SSML, balises xAI, pitch/volume/pause.

## Direction vocale

Chaque segment a un arc dans `notes` : intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration. `slow` réservé aux choix, aux questions et aux fins. L'action reste plus vive.

## Contrôles

- 86 chunks, graphe `option_*_next` / `default_next` conservé
- 27 chemins, 27 fins textuellement distinctes
- 456 à 496 mots par chemin, moyenne 470 (N1, ≥ 3 min d'écoute)
- `check()` OK (N1 ≤ 10 mots/phrase)
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis sur les 86 chunks

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
