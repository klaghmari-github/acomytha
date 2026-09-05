# TREE-AUT-033 — La gouttière du kiosque et le manteau bleu

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Papa frotte le banc mouillé. Le zinc du kiosque répond, ploc. Une virgule de zinc pend, pointe le bouton du manteau bleu. Nino veut les dernières gouttes dans le seau jaune, avant que le kiosque se taise. Il lève trop vite : l'anse glisse, le seau tape, la virgule saute sur le bouton. Au bac, au toboggan ou aux balançoires, la première idée rate. Il reprend le seau. Ballon, seau ou doudou : une flaque ment, la virgule dit vrai. Il refuse de foncer. Filet, fontaine ou grille, le tissu se coince, avance, s'arrête. Il soulève sans tirer. Le ploc et la virgule paient le début. Le manteau garde une trace.

## Arc dramatique

- Monde : parc, kiosque à pain, zinc, banc mouillé, sac de croûte.
- Désir : attraper les gouttes du zinc dans le seau, maintenant.
- Objet : seau jaune (anse rêche) et manteau bleu (boutons ronds).
- Indice unique : la virgule de zinc, vue dès l'ouverture, payée au climax.
- Urgence douce : le zinc se tait, le pain attend.
- Imprévu 1 : anse mouillée, seau qui glisse, sable qui boit.
- Cue : la virgule, pas la force. Un merci vécu.
- Imprévu 2 (plus rusé) : la flaque ou l'ombre ment ; la virgule mène.
- Revers allongé : coincé, corps (envie et peur), refus de foncer, manche qui avance puis s'arrête, geste neuf.
- Résolution : soulever sans tirer, au filet, à la fontaine, à la grille.
- Retour : pain, ploc, virgule, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (papa frotte, le zinc répond), pas un gabarit v2.
- Le premier choix n'enlève pas le seau : il vient au jeu. Le manteau reste visible.
- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.AFF.003 vécue (reprendre seau et manteau), jamais dite.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Nino, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience au départ, petit découragement quand le seau résiste ou disparaît, fierté calme quand Nino soulève sans tirer. L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 683 à 697 mots par chemin, moyenne 690
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N1 ≤ 10 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
