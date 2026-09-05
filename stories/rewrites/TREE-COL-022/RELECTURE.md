# TREE-COL-022 — Le grain de sel et le panier de Nina

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés. Graphe source conservé (boulangerie / étal / fromagerie ; boulangère / voisin / maîtresse ; pain / pomme / fromage).

## Promesse narrative

Sous le store rayé, sur l'allée des planches, un rond d'huile brille. Un grain de sel y tient, blanc. Nina veut le porter dans son panier de toile jusqu'aux tomates, maintenant. Elle parle pendant que papa compte les pièces : personne n'entend. Elle attend, papa s'accroupit, on l'écoute. Le panier part avec elle. La boulangère, le voisin ou la maîtresse (présente, sans rôle parlé) allongent le revers : envie de couper, retenue, rond d'huile menacé, Nina refuse de foncer. Pain, pomme ou fromage reçoivent le grain au centre d'un rond d'huile qui paie l'ouverture. Le rond du début pâlit, vide.

## Vécu

- Désir : porter le grain de sel dans le panier jusqu'aux tomates.
- Imprévu 1 : parole coupée par les pièces ; grain qui glisse.
- Imprévu 2 (plus rusé) : torchon / sac / deux voix, rond d'huile menacé, Nina refuse de foncer, observe l'indice du début.
- COL.POL.001 vécu : envie de couper, retenue, écoute réelle, plaisir d'être entendu. Jamais dit comme règle. Adulte conversationnel.
- Merci vécu : « Merci d'avoir attendu. » (papa, ouverture).
- 27 fins distinctes. Chemins 679–698 mots (moyenne 688).

## Vu et corrigé

- Titre noyau conservé. Troupe D16 : Nina, papa, maman. Pas de 2e enfant.
- 86 nœuds, graphe et libellés d'options conservés (y compris « la maîtresse »).
- Pas de rôle `maîtresse|` : elle est dans la file, papa/maman parlent.
- 27 fins, 27 T3, 9 T2 textuellement distincts.
- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.
- Objet nommé : grain de sel (blanc, minuscule, papier, mission).
- Équipement : panier de toile, cordon rouge — part AVEC dès T1.
- Coin inventif : l'allée des planches, sous le store rayé.
- Indice unique dès l'ouverture : rond d'huile, payé au climax. Pas le grain de sel (objet-titre).
- Monde ≠ TREE-AUT-045 (osier, paprika), ≠ TREE-DIF-008 (cannelle, stores couleur), ≠ TREE-COL-027 (toiles, osier), ≠ TREE-COL-035 (goutte, trois mots, farine).
- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).
- `slow` réservé aux choix, à l'indice et aux fins.
- N3 ≤ 16 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».
- Pas de refrains example3. Pas de merle / miel. Pas apply. Pas audio.

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. Tours de parole : envie de couper, retenue, écoute réelle, plaisir d'être entendu.

## Contrôles

- 86 chunks, graphe `option_*_next` / `default_next` conservé
- 27 chemins, 27 fins textuellement distinctes
- 679 à 698 mots par chemin, moyenne 688 (N3)
- `check()` OK (N3 ≤ 16 mots/phrase)
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` enrichis sur les 86 chunks

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
