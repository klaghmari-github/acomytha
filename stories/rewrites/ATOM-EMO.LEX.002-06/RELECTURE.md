# ATOM-EMO.LEX.002-06 — Chouchou et la petite fleur

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans
- **Leçon :** EMO.LEX.002 — nommer la tristesse + câlin (vécue : vent couche la tige, sourire parti, yeux chauds, papa accroupi, Chouchou dit « je suis triste », demande un câlin ; 2e ruse : dessin qui se déchire au salon, il refuse de foncer). JAMAIS dite en slogan. Pas « j'ai dit : je suis ». Pas « pleurer est permis ».
- **Personnages :** Chouchou, papa, maman. Dump Félix → Chouchou. Dump `enfant-m` + Q « Que dit-il ? » conservés (garçon pour cet atome). Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.
- **Lieu :** jardin, puis salon. Dump : fleur, vent, dessin, crayon, tige, terre. Indice PAS treille / tuteur / feuille / panier (haie n'est pas un tuteur).
- **Indice unique :** éclat de haie (luit près des fleurs → tremble à la chute → luit derrière la vitre au salon → tient près des fleurs). BAN éclat de treille / tuteur / feuille / panier / fauteuil / paillasson / coffre / couverture / capuche / gomme / berge / brouette / housse.
- **Question moteur :** « Chouchou a les yeux chauds. Que dit-il ? » expected dump **triste**. accepted dump `triste | je suis triste | câlin | un câlin | pleurer`. retry dump Félix → Chouchou. Hors Q : null. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

La terre du jardin sent le soleil. Vélo loin. Près des fleurs, un éclat de haie luit. Chouchou veut donner l'eau **maintenant**. Le vent couche la tige. Il tire trop vite. Sourire parti. Yeux chauds. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. Deuxième ruse : le dessin se déchire au salon. Il s'arrête, lit l'éclat derrière la vitre. Un éclat de haie tient près des fleurs. Tige un peu molle, papier fendu. La fin a failli.

## Arc dramatique

- Monde : jardin connu, coin de la haie, terre chaude, verre d'eau, puis salon et table.
- Désir : donner l'eau à la petite fleur, maintenant.
- Objet : petite fleur (tige verte, tête jaune), puis dessin au crayon rouge.
- Indice unique : éclat de haie, vu dès l'ouverture, payé près des fleurs. Pas éclat de treille / tuteur / feuille.
- Urgence douce : il penche le verre, le vent arrive, il tire trop vite.
- Imprévu 1 : vent couche la tige, sourire parti, yeux chauds, une larme.
- Cue : papa à la même hauteur. Un merci vécu, après qu'il refuse de foncer vers la porte.
- Imprévu 2 (plus rusé) : dessin qui se déchire au salon, le coin se fend.
- Résolution : il refuse de foncer, observe, écoute le salon, retrouve l'éclat, demande un câlin, lisse le papier.
- Retour : tige un peu redressée, dessin fendu, éclat près des fleurs. La fin a failli (la tige a plié, le papier s'est fendu).

## Vécu

Chouchou veut donner l'eau **maintenant**. Impatience, puis tige couchée, sourire parti, yeux chauds. Il dit je suis triste, demande un câlin, se blottit. Papa se baisse, pose une question, ne récite pas « pleurer est permis ». Ils agissent : marche sans se presser, dessin, papier qui se fend, il s'arrête. Merci vécu. Fin : l'éclat du début tient près des fleurs.

## Vu et corrigé

- Titre : Chouchou et la petite fleur (noyau dump). Relance : Que dit-il ? expected triste.
- Lieu du dump-meta (jardin, puis salon). Maman et papa. Chouchou = héros enfant-m (dump + Q masculine). Dump fleur / vent / dessin gardés comme objets, pas comme indice.
- Ouverture inventée (terre du jardin, coin qui brille, éclat de haie), pas un gabarit v2, pas « Un escargot avance sur la pierre », pas « Chouchou joue au salon ».
- Indice unique : éclat de haie ×4. BAN éclat de treille / tuteur / feuille / panier / fauteuil / paillasson / coffre / couverture / capuche / gomme / berge / brouette. Pas tache/flèche/marque/symbole. Haie n'est pas un tuteur.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doucement » du dump.
- Leçon non dite : on la voit quand les yeux sont chauds, quand il dit je suis triste, quand il demande un câlin. Pas « pleurer est permis ». Pas « j'ai dit : je suis ». Une seule « je suis triste ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur conservée. expected/accepted dump. retry Félix → Chouchou. Hors Q : null. 5 chunks, kinds inchangés.
- example4 066 / 098 / 030 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le dessin qui se déchire.
- 842 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 842 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
