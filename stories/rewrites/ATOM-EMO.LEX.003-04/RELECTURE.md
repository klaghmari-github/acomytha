# ATOM-EMO.LEX.003-04 — Le moulinet de Mila

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans
- **Leçon :** EMO.LEX.003 — nommer la déception + autre idée (vécue : plus de cerf-volant bleu, épaules basses, gorge serrée, sourire parti, papa accroupi, Mila dit je suis déçue, choisit le moulinet jaune ; 2e ruse : plus de farine au jardin, elle refuse de foncer, tartines au miel). JAMAIS dite dans le récit. Pas « j'ai dit : je suis ». Pas « tu as nommé ». Pas « ce n'est pas honteux ». Pas « on nomme : déçue ».
- **Personnages :** Mila, papa, maman. Dump Cléa → D16 Mila = enfant-f (veut le cerf-volant maintenant). Dump papa + maman ajoutée (check papa/maman parlent). Pas de copain. Troupe D16. Pas de maîtresse.
- **Lieu :** marché puis jardin (2 lieux). Stand des ailes, table de bois. Cerf-volant / moulinet / farine / miel = dump. Miel = tartines (objet), pas le tic « lumière couleur de miel ». BAN cagette / kiosque / étal / citron.
- **Indice unique :** éclat de ficelle (luit à l'ouverture → tremble quand le bleu manque → luit au jardin, plus de farine → tient sur le bois). BAN éclat de farine / miel / cagette / kiosque / étal / citron / pelle / paillasson / fauteuil / coffre / haie / housse / capuche / couverture.
- **Question moteur :** « Le cerf-volant n'est plus là. Que dit Mila ? » expected dump **déçu**. accepted dump `déçu | déçue | je suis déçue | autre idée | un moulinet | une autre idée`. retry dump Cléa → Mila. Non récitée dans les autres chunks. Hors Q : expected / accepted / retry = null.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Les pièces de papa cliquettent. Le sac de pain craque. Le vent tire une ficelle blanche. Sur le bois, un éclat de ficelle luit. Miel collant. Mila veut le cerf-volant bleu **maintenant**. Le stand est vide. Épaules. Gorge. Sourire parti. Papa s'accroupit. Je suis déçue. Un moulinet jaune. Merci vécu. Deuxième ruse : sachet de farine plat. Elle s'arrête, lit l'éclat. Tartines au miel. Un éclat de ficelle tient sur le bois.

## Arc dramatique

- Monde : marché, pièces, sac de pain, ficelle au clou, pots de miel. Puis jardin, table de bois.
- Désir : le cerf-volant bleu, maintenant.
- Objet : cerf-volant manquant, puis moulinet jaune, puis tartines au miel.
- Indice unique : éclat de ficelle, vu dès l'ouverture, payé sur le bois. Pas éclat de farine / miel / cagette.
- Urgence douce : elle veut le bleu tout de suite.
- Imprévu 1 : plus d'aile, poitrine trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après le moulinet.
- Imprévu 2 (plus rusé) : plus de farine, gâteau impossible.
- Résolution : elle refuse de foncer, observe, écoute le jardin, retrouve l'éclat, propose des tartines.
- Retour : moulinet près du pot, pale à trace de miel, éclat sur le bois. Dénouement qui a failli : le sachet était vide.

## Vécu

Mila veut le bleu **maintenant**. Impatience, puis stand vide, sourire parti. Elle dit je suis déçue, regarde le moulinet. Papa se baisse, pose une question, ne récite pas la règle. Jardin, plus de farine. Elle refuse de foncer. Tartines. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Le moulinet de Mila (noyau dump). Relance : Que dit Mila ? expected déçu.
- Lieu du dump-meta (marché puis jardin). Maman ajoutée et papa. Mila = héros enfant-f. Dump Cléa retiré.
- Ouverture inventée (pièces qui cliquettent, sac de pain), pas un gabarit v2, pas « Cléa marche au marché ».
- Indice unique : éclat de ficelle. BAN éclat de farine / miel / cagette / kiosque / étal / citron / pelle / paillasson / fauteuil / coffre / haie / housse / capuche / couverture. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doux » du dump. Strip « j'ai dit : je suis ». Miel objet (tartines) conservé, pas lumière couleur de miel.
- Leçon non dite : on la voit quand les épaules tombent, quand elle dit je suis déçue, quand elle prend le moulinet, quand elle propose des tartines. Pas « ce n'est pas honteux ». Pas « on nomme : déçue ». Pas « Bravo, Mila ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Le cerf-volant n'est plus là. Que dit Mila ? ». expected déçu. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Cléa → Mila. Hors Q : null.
- example4 071 / 003 / 035 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3 / raw.js.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le placard vide.
- 818 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 818 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
