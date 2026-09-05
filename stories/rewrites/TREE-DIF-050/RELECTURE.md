# TREE-DIF-050 — Les deux cerceaux d'Aniss, jusqu'à la porte jaune

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Mila saute sur un pied, face à la porte jaune. Aniss tient le cerceau orange. Un grain de brique s'est coincé dans le bois ; le seuil a un trou de la même taille. Aniss veut les deux cerceaux jusqu'à la porte, tout de suite. Il pousse trop vite : le grand part, le petit reste. Mila ne dit rien. Son silence tient, comme une réponse. Le sourire disparaît. Papa s'accroupit : sans elle, ou avec elle ? Grand, petit ou bâton : les trois partent. Terre, herbe du tilleul ou perron : une pente, un couloir, une marche veulent le laisser seul. Il refuse de foncer. Le grain retrouve son trou. Les cerceaux portent une trace.

## Arc dramatique

- Monde : chemin du village, seuil de brique, porte jaune.
- Désir : faire arriver les deux cerceaux à la porte, avec Mila.
- Objet : grand cerceau orange (grain de brique), petit bleu, bâton.
- Indice unique : le grain de brique, vu dès l'ouverture, payé au climax.
- Urgence douce : le grain doit retrouver le trou du seuil, au soleil.
- Imprévu 1 : Aniss pousse trop vite ; le grand tombe, Mila reste.
- Cue : papa s'accroupit. Un merci vécu (tu l'as attendue).
- Imprévu 2 (plus rusé) : pente, couloir, marche qui finiraient sans elle.
- Revers : silence de Mila, corps, refus de foncer, grain retrouvé.
- Résolution : mains, pont, rouler, couloir, écarter, porter, recevoir, marche.
- Retour : grain dans le trou, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (deux rythmes face à la porte), pas un gabarit v2.
- Le premier choix n'enlève pas l'équipement : les trois affaires partent.
- Déclencheur : les deux enfants ne veulent pas la même chose au même moment.
- Silence de Mila = réponse. Rythmes distincts, sans voix caricaturale.
- Neuf obstacles T2, vingt-sept résolutions, vingt-sept fins.
- Leçon DIF.COR.001 vécue (avancer avec l'autre, respecter son rythme), jamais dite.
- Monde ≠ TREE-DIF-044 groseilles/treillis, ≠ TREE-DIF-056 statue/bronze, ≠ TREE-DIF-045 école/galet/poisson.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Aniss, Mila, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience d'Aniss au départ, petit découragement quand le cerceau tombe ou que Mila s'arrête, fierté calme quand il refuse de foncer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 569 à 589 mots par chemin, moyenne 581
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N2 ≤ 15 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
