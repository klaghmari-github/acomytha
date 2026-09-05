# TREE-AUT-045 — Le panier d'osier de Nina au marché

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Un grain de paprika tient dans l'osier, au clou près de la porte. Nina connaît ce clou ; le grain rouge paraît nouveau. Elle veut porter le panier au marché, pour les fraises, avant que le volet du boulanger se taise. Elle tire trop vite : le panier résiste. Le sourire disparaît. Papa s'accroupit. On décroche, puis on part, le panier avec eux. Pomme, yaourt ou pain : à la main ça glisse ; dans le panier, ça tient. Ballon, seau ou doudou : un rond, un large, un clou mentent. Elle refuse de foncer. Rouge, bleu ou vert, le panier se perd parmi la couleur. Le grain reparaît. Elle choisit une seule chose. L'osier garde une trace.

## Arc dramatique

- Monde : maison puis marché, pavés, fraises, volet du boulanger, panier au clou.
- Désir : porter le panier d'osier au marché, pour les fraises, avant le volet.
- Objet : panier d'osier (grain de paprika), plus pomme / yaourt / pain.
- Indice unique : le grain de paprika, vu dès l'ouverture, payé au climax.
- Urgence douce : le volet du boulanger peut se taire ; les fraises partent.
- Imprévu 1 : le panier résiste au clou ; la nourriture glisse hors de la main.
- Cue : le panier est là. Un merci vécu.
- Imprévu 2 (plus rusé) : ballon-fruit, seau trop large, doudou au clou.
- Revers allongé : coincé, corps (envie et peur), refus de foncer, grain.
- Résolution : regarder l'osier, une seule chose, sans tout prendre.
- Retour : grain de paprika, panier près de la porte, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (le grain dans l'osier, pavés mouillés sans « encore »).
- Le premier choix n'enlève pas le panier : la nourriture entre dedans.
- Revers allongé : coincé, corps, refus, second arrêt, geste lent.
- Neuf obstacles T2 distincts, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.ROU.001 vécue (une chose, puis l'autre), jamais dite.
- Monde ≠ TREE-AUT-046 (Victorino, sac jaune, laitue), ≠ TREE-COL-017 (Amir, pain, virgule farine).
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Nina, papa, maman. Pas de 2e enfant.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience de Nina au départ, petit découragement quand le panier résiste ou que l'objet ment, fierté calme quand elle regarde sans foncer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 645 à 653 mots par chemin, moyenne 648
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N1 ≤ 10 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
