# TREE-AUT-007 — Le volet de Victorina

- **Nouveau titre :** *Le volet de Victorina*
- **Public :** 5–6 ans (N3), lecture interactive familiale
- **Leçon principale :** AUT.ROU.001 — une chose, puis la suivante (vécue, non dite)
- **Personnages :** Victorina, papa, maman
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

## Promesse narrative

Victorina a glissé un oiseau de papier entre les lattes. Au matin, elle veut ouvrir le volet tout de suite : la rue, le moineau, le pain. Elle tire trop vite, le bois gonflé fait clac. Chambre, savon ou cuisine changent l'obstacle ; t-shirt, chaussettes ou gilet changent le corps ; sac, manteau ou doudou changent le geste. Le volet s'ouvre quand elle finit une chose avant l'autre. À table, le pain paie le début.

## Améliorations appliquées

- Monde (bois jaune, fente de soleil, pain, moineau) avant l'action.
- Désir immédiat (ouvrir, libérer l'oiseau) distinct de la leçon.
- Première idée échoue : tir trop fort, pieds nus, bois gonflé.
- T1/T2/T3 changent l'action, pas seulement le lieu.
- 27 fins textuellement distinctes, dernière image unique.
- Un merci (ouverture) et un bravo vécu (chambre), pas un refrain.
- Pas de « une étape après l'autre », pas Maya, pas apply.

## Direction vocale

TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc.

## Contrôles

- 86 chunks
- 27 chemins, 590 à 631 mots, moyenne 608
- 27 fins et 27 dernières images distinctes
- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés
- N3 ≤ 16 mots/phrase. `check()` OK.

## Relu

P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène (volet / mains / pain). Option labels conservés.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
