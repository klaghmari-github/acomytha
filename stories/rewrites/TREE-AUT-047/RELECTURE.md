# TREE-AUT-047 — Le manteau de Raphaël près des bottes

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Les clés de papa tombent dans la coupelle. Raphaël lève les yeux : le paillasson est mouillé, les bottes jaunes brillent, et sur le cuir gauche une écaille de boue blonde tient, plate, un peu sèche. Il veut sortir maintenant. Il tire trop vite : l'air froid lui prend les bras. Le sourire disparaît. Papa s'accroupit. Cuisine, jardin ou chambre : sans le manteau le froid gagne ; le bleu part avec lui. Cubes, livre ou dînette : un bol, un torchon, un arrosoir, un seau, un gant, un pyjama, un coussin ou un rideau bleu ment. Il refuse de foncer. Matin, après la sieste ou soir : une chaise, un sol ou une ombre usurpent la place du portemanteau. Il observe, écoute le tic, retrouve l'écaille, accroche près des bottes. Le dénouement a failli. L'écaille paie le début. Le manteau garde une trace.

## Arc dramatique

- Monde : entrée, paillasson mouillé, bottes jaunes, portemanteau.
- Désir : sortir jouer maintenant, avant que l'écaille sèche.
- Objet : manteau bleu (fermeture à tic), près des bottes.
- Indice unique : l'écaille de boue blonde, vue dès l'ouverture, payée au climax.
- Urgence douce : l'air froid, l'écaille qui sèche au bord.
- Imprévu 1 : il tire sans le bleu ; le froid gagne les bras.
- Cue : papa ou maman s'accroupit. Un merci vécu.
- Imprévu 2 (plus rusé) : un faux bleu, puis une fausse place (chaise, sol, ombre).
- Revers allongé : coincé, corps (envie et inquiétude), refus de foncer, écoute du tic, geste neuf.
- Résolution : accrocher près des bottes, cubes / livre / dînette, matin / sieste / soir.
- Retour : écaille de boue blonde, bottes jaunes, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (les clés dans la coupelle), pas le dump « Le paillasson de l'entrée est encore mouillé ».
- Le premier choix n'enlève pas le manteau : il part avec Raphaël.
- Revers allongé : coincé, corps, refus, second arrêt, geste lent.
- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.AFF.002 vécue (accrocher près des bottes), jamais dite.
- Monde ≠ TREE-AUT-032 (Mila, manteau vert, casserole), ≠ TREE-AUT-037 (Chouchou, manteau jaune, gouttière), ≠ TREE-DIF-003 (Mila, manteau à pois).
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Raphaël, papa, maman. Un seul enfant.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience de Raphaël au départ, petit découragement quand le manteau résiste ou qu'un faux bleu ment, fierté calme quand il accroche sans foncer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 673 à 690 mots par chemin, moyenne 681
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N2 ≤ 15 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
