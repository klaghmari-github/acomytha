# TREE-COL-033 — La chaîne tiède et le galet

- **Public :** N2, 4–5 ans, lecture interactive familiale
- **Leçon :** COL.ECO.001 — écouter à l'école, en parler à la maison (implicite)
- **Secondaire :** COL.POL.001 — demander avec attention (implicite)
- **Personnages :** Nino, papa, maman
- **Lieu :** parc du village, après l'école, chaîne de balançoire, galet
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Après l'école, Nino veut pendre son galet à la chaîne tiède, comme une clochette, et donner à papa et maman le mot qu'il a gardé près des crochets. Sa première phrase se perd dans la fermeture du cartable ; le galet roule. Le bac, le toboggan ou les balançoires changent l'échec. Le ballon, le seau ou le doudou changent la manière de récupérer la pierre. Le banc, la poche ou la paume décident où le mot atterrit. Le soir, la chaîne n'a plus besoin de clochette.

## Vécu

Nino veut la clochette **maintenant**, et dire le mot tout de suite. Il coupe. Personne n'entend. Le galet file. Le ventre se serre. Il touche une manche, attend un filet, un visage, un tic qui s'arrête, puis on l'écoute. La leçon se voit : parler dans les mots des autres perd le galet ; attendre la fin de la phrase livre le mot des crochets. Pas de « on écoute la maîtresse » récité.

## Améliorations

- Titre noyau conservé. Kenzo → Nino. Parc après l'école, pas calque COL-015 (pas d'escargot, pas de dîner-soupe).
- Première tentative ratée dès l'ouverture (fermeture du cartable, galet sous le banc).
- T1/T2/T3 changent l'obstacle, pas seulement le décor.
- T3 Tom/Léa/Sami → le banc, la poche, la paume.
- Refrains « on va apprendre / voici le geste / si malaise on raconte / Bravo bon travail / l'histoire est finie » retirés.
- Un merci vécu, lié au geste (attendre le filet, les visages, la chaîne).
- 27 fins textuellement distinctes : chaîne + place unique du galet + mot entendu.
- TTS par fonction (opening / choice / clue / confirm / action / obstacle / resolution / ending).
- Mots par chemin : 719–768 (moyenne 744).

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

