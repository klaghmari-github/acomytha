# TREE-AUT-005 — Le coq et les bottes de Raphaël

Réécriture éditoriale F-NAR-019. Graphe, `chunk_id`, types de blocs et destinations techniques inchangés.

## Promesse narrative

Après la pluie, le volet bleu de la ferme tape toc. Le coq a chanté une fois derrière la grange, puis s'est tu. Raphaël veut le rejoindre maintenant, avec un ballon rouge, un seau bleu de grain ou son doudou. Le chemin de terre est mouillé : les chaussons échouent, les bottes passent, gauche puis droite. Chat, chien ou poule font quelque chose d'inattendu. La première idée rate. L'animal montre trois coins nommés dans la ferme : le secret du cabanon, le fournil, les tomates. Raphaël comprend sans forcer le coq. Le toc du loquet paie le volet du début. Les bottes gardent boue et paille.

## Arc dramatique

- Monde : ferme, volet bleu, paille, grange, chemin de terre mouillé.
- Désir : rejoindre le coq avant qu'il se cache.
- Objet : ballon / seau de grain / doudou, plus les bottes (équipement).
- Urgence douce : le chant s'est arrêté.
- Imprévu 1 : sortir pieds nus, objet qui glisse, pierre froide.
- Cue : botte gauche, puis droite. Un merci vécu.
- Imprévu 2 (plus rusé) : l'animal ne se laisse pas faire ; il montre.
- Résolution : attendre, poser l'objet, ne pas forcer le coq.
- Retour : toc, paille, boue, objet marqué, 27 souvenirs distincts.

## Corrections éditoriales

- Le premier choix n'enlève pas les bottes : objet compagnon, puis bottes.
- T3 n'est plus un simple moment de la journée : cabanon / fournil / tomates.
- Neuf obstacles animaux distincts, vingt-sept résolutions, vingt-sept fins.
- Leçon AUT.ROU.001 vécue (gauche puis droite, puis le chemin), jamais dite.
- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.
- Troupe D16 : Raphaël, papa, maman.
- Voix : notes + ssml + xai + piper par chunk, profils raw.js.

## Direction vocale

Impatience au départ, petit découragement quand l'objet ou l'animal résiste, fierté calme quand Raphaël agit seul. L'adulte guide peu. `slow` réservé aux choix, à la question, à l'émotion du retour.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins textuellement distinctes
- 27 T3 distincts, 9 T2 distincts
- 623 à 648 mots par chemin, moyenne 634
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis
- `notes` présentes sur les 86 chunks
- N1 ≤ 10 mots/phrase
- check() OK. Pas d'apply. Pas d'audio. Pas de git.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
