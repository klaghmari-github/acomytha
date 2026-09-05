# TREE-AUT-046 — Le sac jaune de Victorino sur le banc

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Le banc de bois craque sans personne : le sac jaune a glissé. Sur la boucle, une dent de laitue tient, froide, collée. Victorino veut ce sac pour le camp de la laitue, avec un goûter, avant que l'escargot touche le cœur vert. Il tire trop vite : le sac retombe, mou, vide. Le sourire disparaît. Papa s'accroupit. Pomme, yaourt ou pain : à la main ça glisse ; dans le sac, ça tient. Cuisine, jardin ou chambre : un torchon, un gant ou un coussin jaune ment. Il refuse de foncer. Cubes, livre ou dînette, la boucle se cache. Il ouvre sans forcer. La dent et le banc paient le début. Le sac garde une trace.

## Arc dramatique

- Monde : jardin, arrosoir, laitue, escargot, banc de bois.
- Désir : porter le sac jaune au camp de la laitue, avant l'escargot.
- Objet : sac jaune (dent de laitue), plus pomme / yaourt / pain.
- Indice unique : la dent de laitue, vue dès l'ouverture, payée au climax.
- Urgence douce : l'escargot avance vers le cœur vert.
- Imprévu 1 : le sac vide retombe ; le goûter glisse hors de la main.
- Cue : le sac est là, sur le bois. Un merci vécu.
- Imprévu 2 (plus rusé) : un faux jaune ment ; la dent dit vrai.
- Revers allongé : coincé, corps (envie et peur), refus de foncer, boucle qui avance puis s'arrête, geste neuf.
- Résolution : ouvrir sans forcer, cubes / livre / dînette.
- Retour : dent de laitue, banc de bois, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (le banc craque sans personne), pas un gabarit v2.
- Le premier choix n'enlève pas le sac : le goûter entre dedans.
- Revers allongé : coincé, corps, refus, second arrêt, geste lent.
- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.AFF.001 vécue (glisser dans le sac), jamais dite.
- Monde ≠ TREE-COL-002 banc de fer Amir, ≠ TREE-COL-023 banc pomme Mila, ≠ TREE-COL-017 escargot boulangerie.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Victorino, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience de Victorino au départ, petit découragement quand le sac retombe ou disparaît, fierté calme quand il ouvre sans forcer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 654 à 675 mots par chemin, moyenne 664
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N2 ≤ 15 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
