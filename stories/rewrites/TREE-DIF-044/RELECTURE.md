# TREE-DIF-044 — Les groseilles de Raphaël au treillis

Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Un grain rouge tombe dans le bol blanc, vide, près de la marche. Le treillis de fer fait tic en séchant : un grain de grenat y reste collé. Raphaël veut remplir le bol pour le goûter, tout de suite. Sarah reste sur la marche, ciré trop long. Le silence répond. Le sourire disparaît. Papa s'accroupit. Bol, panier ou nappe : il part trop vite, elle dit attends, les trois partent. Serre, tilleul ou treillis : il tire, elle pose sa limite, la première cueillette rate. Il refuse de foncer. Torchon, mains, pas hors de la serre ; élastique, serviette, Sarah tient le bol ; manches, panier, nœud. Le grain de grenat paie le début. Le bol rentre avec une trace.

## Arc dramatique

- Monde : jardin après la pluie, serre, tilleul, treillis de fer.
- Désir : remplir le bol de groseilles pour le goûter, avec Sarah.
- Objet : bol blanc / panier d'osier / nappe à carreaux (les trois partent).
- Indice unique : le grain de grenat collé au treillis, vu dès l'ouverture, payé au climax.
- Urgence douce : les grains vont sécher, le pain attend.
- Imprévu 1 : Raphaël part trop vite ; Sarah reste ; la cueillette rate.
- Cue : papa s'accroupit. Un merci vécu (tu as attendu Sarah).
- Imprévu 2 (plus rusé) : reflet / feuille-grain / ombre de fil ; le silence de Sarah.
- Revers : corps (sourire disparu, poitrine), refus de foncer, indice retrouvé.
- Résolution : cueillir avec elle, à son pas, selon le geste choisi.
- Retour : grain de grenat, 27 traces distinctes.

## Corrections éditoriales

- Ouverture inventée (un grain tombe dans un bol vide), pas le gabarit v2, pas « Un merle saute ».
- Le premier choix n'enlève pas le contenant : bol, panier et nappe partent.
- Labels T1/T2/T3 conservés. Leçon DIF.COR.003 vécue (rythmes, limite, silence), jamais dite.
- Neuf T2 distincts, vingt-sept T3, vingt-sept fins.
- Monde ≠ TREE-DIF-065 (Chouchou, arrosoirs), ≠ TREE-DIF-056 (statue de bronze), ≠ TREE-DIF-052 (grain d'ambre, mer).
- Pas de refrain example3, pas de miel, pas de gouttes-refrain, pas de grand-père/maîtresse.
- Tics « encore / déjà / tout doux / tout calme » retirés.
- Troupe D16 : Raphaël, Sarah, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience de Raphaël au départ, petit découragement quand Sarah s'arrête, fierté calme quand il cueille sans la tirer. Le silence de Sarah compte. `slow` réservé aux choix, à la question, au retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 668 à 697 mots par chemin, moyenne 683
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N2 ≤ 15 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
