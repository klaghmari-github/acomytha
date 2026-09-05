# TREE-AUT-022 — La pomme dans l'herbe

Réécriture éditoriale F-NAR-019. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

La pâte sent, le saladier blanc est vide : il manque la quatrième pomme. Sous le pommier, une pomme rouge porte une feuille-œil (trou rond). Un manteau bleu à boutons de bois attend sur le banc. Aniss court trop vite, sans l'enfiler : la manche se tord, l'herbe pique. Cuisine, jardin ou chambre, il met le manteau. Cubes, livre ou dînette : un faux rouge ment. Matin, sieste ou soir, il refuse de foncer, regarde par le trou, porte le fruit, raccroche. Le toc et le saladier paient le début.

## Arc dramatique

- Monde : jardin du pommier, coin de la tarte, saladier vide.
- Désir : porter la quatrième pomme avant que le four n'attende trop.
- Objet : pomme rouge à feuille-œil, manteau bleu (toc), plus cubes / livre / dînette.
- Urgence douce : le plat ne peut pas attendre.
- Imprévu 1 : manteau mal pris, herbe froide, pomme qui roule.
- Cue : enfiler le manteau, regarder le trou. Un merci vécu.
- Imprévu 2 (plus rusé) : un faux rouge (cube, image, jouet) ment ; la feuille-œil dit vrai.
- Résolution : refuser de foncer, regarder par le trou, selon la lumière.
- Retour : toc, saladier plein, 27 traces distinctes.

## Corrections éditoriales

- Le premier choix n'enlève pas le manteau : il vient jusqu'à la pomme.
- Déclencheur : un ingrédient manque (la quatrième pomme, le saladier vide).
- Neuf fausses pommes distinctes, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.AFF.002 vécue (mettre le manteau pour sortir), jamais dite.
- Pas de refrain example3/v2, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Aniss, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience au départ, petit découragement quand le manteau résiste ou qu'un faux rouge ment, fierté calme quand Aniss regarde par le trou et porte le fruit. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 666 à 691 mots par chemin, moyenne 676
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N3 ≤ 16 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
