# TREE-AUT-021 — Le grain de sable dans la sangle

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Le vent de l'eau pousse la porte : la chaise de paille craque. Sur la sangle du sac roux, une écaille de nacre tient, lisse, un peu rose. À côté, un grain de sable pique. Mila veut l'eau tout de suite. Elle tire trop vite : le grain pique, le sac glisse, elle secoue trop fort. Le grain vacille. Papa s'accroupit. Bac, toboggan ou balançoires : le sac vient. Ballon, seau ou doudou : à la main ça file vers l'eau ; dans le sac, ça tient. Banc, cabine ou galets : un faux éclat ment, l'écaille dit vrai. Elle refuse de foncer. Elle glisse sans secouer. L'écaille et le grain paient le début. Le sac garde une trace.

## Arc dramatique

- Monde : maison près de la mer, chaise de paille, bord de l'eau.
- Désir : porter le sac roux jusqu'à l'eau, garder le grain.
- Objet : grain de sable dans la sangle, plus ballon / seau / doudou.
- Indice unique : l'écaille de nacre, vue dès l'ouverture, payée au climax.
- Urgence douce : Mila veut l'eau tout de suite.
- Imprévu 1 : le grain pique, le sac glisse, elle secoue trop fort.
- Cue : le sac est là. Un merci vécu.
- Imprévu 2 (plus rusé) : écume / crochet / galet mentent ; l'écaille dit vrai.
- Revers allongé : coincé, corps (envie et peur), refus de foncer, geste neuf.
- Résolution : ouvrir sans secouer, glisser le jouet dans le sac.
- Retour : écaille de nacre, grain dans la sangle, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (le vent de l'eau pousse la porte), pas un gabarit v2.
- Pas « Le sac bleu attend », pas « sandales encore mouillées ».
- Le premier choix n'enlève pas le sac : il vient aux trois coins.
- Revers allongé : coincé, corps, refus, second arrêt, geste lent.
- Neuf T2 distincts, vingt-sept T3, vingt-sept fins.
- Leçon AUT.AFF.001 vécue (glisser dans le sac, garder le grain), jamais dite.
- Monde ≠ TREE-AUT-009 sac bleu salon, ≠ TREE-AUT-046 sac jaune laitue.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Mila, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience de Mila au départ, petit découragement quand le sac glisse ou le jouet file, fierté calme quand elle glisse sans secouer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 670 à 691 mots par chemin, moyenne 677
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N2 ≤ 15 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
