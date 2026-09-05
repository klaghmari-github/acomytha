# ATOM-EMO.LEX.002-04 — Raphaël et la tour de cubes

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans
- **Leçon :** EMO.LEX.002 — nommer la tristesse + câlin (vécue : cubes tombent, gorge serrée, yeux chauds, sourire parti, papa accroupi, Raphaël dit je suis triste, pleure, demande un câlin, pull de papa sent le pain ; 2e ruse : chat revient, cube qui roule, il refuse de foncer, petite tour recommence). JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « j'ai dit : je suis ».
- **Personnages :** Raphaël, papa, maman. Dump Mateo → D16 Raphaël = enfant-m (veut la tour maintenant). Chat du dump = imprévu. Pas de copain. Troupe D16. Pas de maîtresse.
- **Lieu :** salon, après-midi, cubes, tour, chat, fauteuil, soleil, bois, pain, bol, pull. BAN tapis / canapé / coussin / rideau. Cubes / tour / chat = dump. ≠ dump rideau / tapis.
- **Indice unique :** éclat de fauteuil (luit à l'ouverture → tremble aux larmes → luit quand le chat revient et le cube roule → tient sur le tissu). BAN éclat de cube / tour / tapis / canapé / coussin / treille / moule / tuteur / saladier / gomme / berge / brouette / couverture / capuche / paillasson.
- **Question moteur :** « Raphaël a les yeux chauds. Que dit-il ? » expected dump **triste**. accepted dump `triste | je suis triste | câlin | un câlin | pleurer`. retry dump Mateo → Raphaël. Non récitée dans les autres chunks. Hors Q : expected / accepted / retry = null.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Le chat frotte le dossier, puis s'en va. Le tissu du fauteuil sent le soleil d'après-midi. Sur le tissu, un éclat de fauteuil luit. Cubes bleus et jaunes. Raphaël veut la tour **maintenant**. Il pose trop vite, trop haut. Le chat revient du bol. Sa queue balaie. Les cubes tombent. Gorge serrée. Yeux chauds. Sourire parti. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. Deuxième ruse : cube qui roule, chat qui revient. Il s'arrête, lit l'éclat. Une petite tour recommence. Un éclat de fauteuil tient sur le tissu.

## Arc dramatique

- Monde : salon, après-midi, fauteuil chaud, bol du chat, cubes bleus et jaunes. BAN tapis / canapé / coussin / rideau.
- Désir : empiler la tour, maintenant.
- Objet : cubes, puis tour qui tombe, puis petite tour.
- Indice unique : éclat de fauteuil, vu dès l'ouverture, payé sur le tissu. Pas éclat de cube / tour / tapis / canapé / coussin.
- Urgence douce : il pose trop vite, trop haut.
- Imprévu 1 : queue du chat, cubes par terre, poitrine trop vite, sourire parti, larmes.
- Cue : papa à la même hauteur. Un merci vécu, après le câlin.
- Imprévu 2 (plus rusé) : cube qui roule vers le fauteuil, chat qui revient, petite tour qui penche.
- Résolution : il refuse de foncer, observe, écoute le salon, retrouve l'éclat, pose sans se presser.
- Retour : petite tour près du fauteuil, chat au soleil, éclat sur le tissu. Dénouement qui a failli : le cube roulait, le chat revenait.

## Vécu

Raphaël veut la tour **maintenant**. Impatience, puis cubes par terre, sourire parti. Il dit je suis triste, pleure, demande un câlin. Papa ouvre les bras. Le pull sent le pain. Papa se baisse, pose une question, ne récite pas la règle. Chat revient, cube roule. Il refuse de foncer. Petite tour. Merci vécu. Fin : l'éclat du début tient sur le tissu.

## Vu et corrigé

- Titre : Raphaël et la tour de cubes (noyau dump). Relance : Que dit-il ? expected triste.
- Lieu du dump-meta (salon, après-midi). Maman et papa. Raphaël = héros enfant-m. Chat du dump = imprévu. Dump Mateo retiré.
- Ouverture inventée (chat qui frotte le dossier, puis s'en va), pas un gabarit v2, pas « Le rideau se lève », pas « joue au salon ».
- Indice unique : éclat de fauteuil. BAN éclat de cube / tour / tapis / canapé / coussin / treille / moule / tuteur / saladier / gomme / berge / brouette / couverture / capuche / paillasson. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doucement » du dump.
- Leçon non dite : on la voit quand les yeux sont chauds, quand il dit je suis triste, quand il demande un câlin, quand papa ouvre les bras. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « j'ai dit : je suis ». Pas « Bravo, Raphaël ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Raphaël a les yeux chauds. Que dit-il ? ». expected triste. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Mateo → Raphaël. Hors Q : null.
- example4 064 / 096 / 028 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2 / raw.js.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le chat et le cube qui roule.
- 842 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 842 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
