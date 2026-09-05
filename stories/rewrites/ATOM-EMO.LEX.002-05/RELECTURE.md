# ATOM-EMO.LEX.002-05 — Victorino et le train en bois

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans
- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un câlin (vécue : train perdu, sourire parti, poitrine serrée, yeux chauds, Victorino dit je suis triste, pleure, demande un câlin, papa ouvre les bras ; 2e ruse : Amir rentre chez lui, train toujours perdu, il refuse de foncer, éclat de coffre, papa trouve). JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». Pas « j'ai dit : je suis ».
- **Personnages :** Victorino, Amir, papa, maman. Victorino = héros enfant-m (veut le train maintenant). Amir = copain (deux D16). Troupe D16. Pas de maîtresse.
- **Lieu :** chambre, puis salon. Dump train / bois / wagon / lit / tapis / canapé gardés comme objets, pas comme indice.
- **Indice unique :** éclat de coffre (luit à l'ouverture → tremble aux larmes → luit quand Amir part et le train manque → tient sur le bois). BAN éclat de wagon / bois / lit / tapis / canapé / fauteuil / paillasson / couverture / capuche. Pas treille / moule / tuteur / saladier / gomme / berge / brouette.
- **Question moteur :** « Victorino a les yeux chauds. Que dit-il ? » expected dump **triste**. accepted dump `triste | je suis triste | câlin | un câlin | pleurer`. retry dump Étienne → Victorino. Non récitée dans les autres chunks. Hors Q : expected / accepted / retry nuls.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

La poignée du coffre est tiède, sous la fenêtre. Vernis. Amir près du tapis. Wagon rouge. Sur le couvercle, un éclat de coffre luit. Victorino veut le train **maintenant**, jusqu'au salon. Le train n'est pas là. Sourire parti. Poitrine serrée. Yeux chauds. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. Deuxième ruse : Amir rentre, train toujours perdu. Il s'arrête, lit l'éclat. Papa trouve. Un éclat de coffre tient sur le bois.

## Arc dramatique

- Monde : chambre, poignée tiède, vernis, tapis, lit, wagon.
- Désir : faire rouler le train en bois jusqu'au salon, maintenant, avec Amir.
- Objet : train en bois, wagon, rail, coffre.
- Indice unique : éclat de coffre, vu dès l'ouverture, payé sur le bois. Pas éclat de wagon / bois / lit / tapis / canapé.
- Urgence douce : il fouille trop vite, trop fort.
- Imprévu 1 : train absent, coffre claqué, sourire parti, poitrine serrée, larmes.
- Cue : papa à la même hauteur. Un merci vécu, après le câlin.
- Imprévu 2 (plus rusé) : Amir rentre chez lui, train toujours perdu au salon, coincé sous un rabat.
- Résolution : il refuse de foncer, observe, écoute le salon, retrouve l'éclat. Papa tire tout petit à petit.
- Retour : roue marquée, train contre le coffre, éclat sur le bois. Dénouement qui a failli : Amir est parti, le train faillit rester coincé.

## Vécu

Victorino veut le train **maintenant**. Impatience, puis lit vide, sourire parti. Il dit je suis triste, pleure, demande un câlin. Papa ouvre les bras. Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : chercher sans se presser, porter le coffre, tenir le bord, papa trouve. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Victorino et le train en bois (noyau dump). Relance : Que dit-il ? expected triste.
- Lieu du dump-meta (chambre, puis salon). Maman et papa. Victorino = héros enfant-m. Amir = copain. Dump train / bois / wagon / lit / tapis / canapé.
- Ouverture inventée (poignée tiède, vernis), pas un gabarit v2, pas « Une poussière danse », pas « L'histoire est finie ».
- Indice unique : éclat de coffre ×4. BAN éclat de wagon / bois / lit / tapis / canapé / fauteuil / paillasson / couverture / capuche. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « j'ai dit : je suis », « pleurer est permis ».
- Leçon non dite : on la voit quand les yeux sont chauds, quand Victorino dit je suis triste, quand il pleure, quand il demande un câlin. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « j'ai dit : je suis ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Victorino a les yeux chauds. Que dit-il ? ». expected triste. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Étienne → Victorino. Hors Q : null.
- example4 065 / 097 / 029 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers Amir qui part.
- 833 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 833 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
