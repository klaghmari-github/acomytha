# TREE-AUT-023 — Le manteau sur la rampe

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Le bois de la rampe garde une chaleur : le manteau rouge a choisi sa place. Au col, un croissant de cuivre brille vers le jardin. Chouchou veut le porter au coin des crochets avant que le soleil quitte le bois. Elle tire trop vite : la manche accroche, le sourire disparaît. Papa s'accroupit. Au bac, au toboggan ou aux balançoires, elle pose le manteau pour jouer : première idée, patatras. Elle le reprend. Ballon, seau ou doudou : une ombre rouge ment, le croissant dit vrai. Elle refuse de foncer. Banc, portail ou paillasson, le tissu se coince, avance, s'arrête. Elle soulève sans tirer. Le croissant et le cric paient le début. Le manteau garde une trace.

## Arc dramatique

- Monde : couloir, rampe de bois qui garde la chaleur, fraises, cric, coin des crochets.
- Désir : porter le manteau au crochet, maintenant.
- Objet : manteau rouge (croissant de cuivre), plus ballon / seau / doudou.
- Indice unique : le croissant de cuivre, vu dès l'ouverture, payé au climax.
- Urgence douce : le soleil quitte la rampe.
- Imprévu 1 : manche coincée, tissu qui glisse au jeu.
- Cue : le croissant, pas la force. Un merci vécu.
- Imprévu 2 (plus rusé) : l'ombre du manteau ment ; le croissant mène.
- Revers allongé : coincé, corps (envie et peur), refus de foncer, manche qui avance puis s'arrête, geste neuf.
- Résolution : soulever sans tirer, au banc, au portail, au paillasson.
- Retour : cric, croissant, fraise, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (le manteau a choisi la rampe), pas un gabarit v2.
- Le premier choix n'enlève pas le manteau : il vient au jardin.
- Revers allongé (audit : obstacle trop ponctuel) : coincé, corps, refus, second arrêt, geste lent.
- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.AFF.003 vécue (reprendre le manteau), jamais dite.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Chouchou, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience au départ, petit découragement quand le manteau résiste ou disparaît, fierté calme quand Chouchou soulève sans tirer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 676 à 695 mots par chemin, moyenne 683
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N1 ≤ 10 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
