# TREE-AUT-048 — Le seau rouge de Nina près de la flaque

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Le lampadaire penche son ombre comme une cuillère dans la flaque. Sur l'anse en corde du seau rouge, une perle de verre fait un éclair blanc. Nina veut les ronds du lampadaire dans son seau avant que le soleil les boive. Nino veut sauter dans la même flaque, maintenant. Elle plonge trop vite : les ronds se cassent, le sourire disparaît. Papa s'accroupit. Au bac, au toboggan ou aux balançoires, elle pose le seau pour jouer : première idée, patatras. Elle le reprend. Ballon, seau ou doudou : un faux rouge ment, la perle dit vrai. Elle refuse de foncer. Banc, portail ou haie, l'anse se coince, avance, s'arrête. Elle soulève sans tirer. La perle et le dernier rond paient le début. Le seau garde une trace.

## Arc dramatique

- Monde : parc après la pluie, lampadaire, flaque du chemin, banc de pierre.
- Désir : attraper les ronds du lampadaire dans le seau rouge, maintenant.
- Objet : seau rouge (perle de verre), plus ballon / seau / doudou.
- Indice unique : la perle de verre, vue dès l'ouverture, payée au climax.
- Urgence douce : le soleil boit les ronds.
- Imprévu 1 : Nino saute, le seau plonge trop vite, les ronds se cassent.
- Cue : la perle, pas la force. Un merci vécu.
- Imprévu 2 (plus rusé) : un faux rouge ment ; la perle dit vrai.
- Revers allongé : coincé, corps (envie et peur), refus de foncer, anse qui avance puis s'arrête, geste neuf.
- Résolution : soulever sans tirer, au banc, au portail, à la haie.
- Retour : dernier rond, perle, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (le lampadaire-cuillère), pas un gabarit v2.
- Le premier choix n'enlève pas le seau : il vient au parc.
- Deux enfants, deux désirs : Nina les ronds, Nino le saut.
- Revers allongé : coincé, corps, refus, second arrêt, geste lent.
- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.AFF.003 vécue (reprendre seau, manteau, doudou), jamais dite.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Nina, Nino, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience de Nina au départ, petit découragement quand l'objet résiste ou disparaît, fierté calme quand elle soulève sans tirer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 676 à 696 mots par chemin, moyenne 684
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N1 ≤ 10 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
