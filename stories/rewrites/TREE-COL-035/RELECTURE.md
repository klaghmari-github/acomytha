# TREE-COL-035 — Le store goutteux et les trois mots

- **Public :** N2, 4–5 ans, lecture interactive familiale
- **Leçon :** COL.POL.001 — demander avec attention et respect (implicite)
- **Secondaire :** COL.ECO.002 — attendre son tour de parole (implicite)
- **Personnages :** Raphaël, papa, maman
- **Lieu :** marché sous le store, boulangerie, étal, fromagerie
- **Objet :** panier d'osier troué, anse rêche
- **Indice unique :** croissant d'eau sur la toile rayée, payé au climax
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Sous le store goutteux, Raphaël veut faire arriver trois mots jusqu'au bout, pour remplir le panier. Sa première phrase se casse contre la liste de papa ; une goutte tape sa chaussure. La boulangerie, l'étal ou la fromagerie changent le bruit qui recouvre. La boulangère, le voisin ou la maîtresse changent l'oreille à attendre. Le pain, la pomme ou le fromage changent la trace dans le trou. Il refuse de foncer, guette le toc du croissant d'eau, puis parle dans le silence.

## Vécu

Raphaël veut les trois mots **maintenant**. Il coupe. Personne n'entend. Le sourire disparaît. Envie et inquiétude se bousculent. Papa s'accroupit. Un merci vécu : attendre la phrase. Tours : envie de couper, retenue, écoute réelle, plaisir d'être entendu. La leçon se voit : parler dans les mots des autres casse la phrase ; attendre le toc la livre entière. Pas de « on dit bonjour, on dit s'il te plaît, on dit merci » récité.

## Améliorations

- Titre noyau conservé. Ouverture par un toc, pas un gabarit v2.
- Indice unique dès le début (croissant d'eau), payé à chaque climax T3 et au revers.
- Première tentative ratée dès l'ouverture (liste + goutte sur la chaussure).
- T1/T2/T3 changent l'obstacle, pas seulement le décor.
- Revers allongé : 12 phrases, objet + trou + croissant + toc du début.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Adulte conversationnel (papa/maman). Maîtresse narrée, pas en rôle.
- Un merci vécu, lié au geste (attendre la phrase).
- 27 fins textuellement distinctes.
- TTS par fonction (opening / choice / clue / confirm / action / obstacle / resolution / ending).
- Mots par chemin : 753–786 (moyenne 770).

## Direction vocale

Chaque segment a un `notes` : arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration. `slow` réservé aux choix, indices et fins. Action plus vive. Fins : pitch bas, volume doux, pause longue.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins distinctes, 27 climats T3 distincts, 9 T2 distincts
- `text` = `script` collé, N2 ≤ 15 mots/phrase
- `text_ssml` et `text_xai_tags` enrichis sur les 86 chunks
- graphe `option_*_next` / `default_next` / `kind` inchangés
- `check()` OK

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.

