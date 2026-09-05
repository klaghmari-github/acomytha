# ATOM-EMO.LEX.002-03 — Sarah et le dessin mouillé

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans
- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un câlin (vécue : goutte sur le soleil, sourire parti, poitrine serrée, yeux chauds, Sarah dit je suis triste, pleure, demande un câlin, maman ouvre les bras ; 2e ruse : Nina part plus tôt, dessin mouillé, elle refuse de foncer). JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». Pas « j'ai dit : je suis ».
- **Personnages :** Sarah, Nina, papa, maman. Sarah = héros enfant-f. Nina = copine D16 (deux enfants OK). Troupe D16. Pas de maîtresse. Dump Chloé / Lila → Sarah / Nina.
- **Lieu :** jardin, puis porte de l'école. Dump dessin / goutte / arrosoir / galet gardés. Indice PAS galet / arrosoir / vitre / crayon / gomme / sac / cartable.
- **Indice unique :** éclat de paillasson (luit à l'ouverture → tremble aux larmes → luit à la porte de l'école → tient sur le bord). BAN éclat de galet / arrosoir / treille / moule / tuteur / saladier / gomme / berge / brouette / couverture / capuche / torchon / tabouret. Pas tache/flèche/marque/symbole.
- **Question moteur :** « Sarah est triste. Que peut-elle faire ? » expected dump **triste**. accepted dump `triste | pleurer | un câlin | câlin | demander un câlin`. retry dump Chloé → Sarah. Non récitée dans les autres chunks. Hors Q : expected / accepted / retry nuls.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Sarah connaît la table du jardin. Galet, goutte, arrosoir, menthe. Sur le paillasson, un éclat de paillasson luit. Elle veut finir le soleil pour Nina **maintenant**. Une goutte tombe. Elle souffle trop vite. Sourire parti. Poitrine serrée. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. Deuxième ruse : à la porte de l'école, Nina part plus tôt, le dessin est mouillé. Elle s'arrête, lit l'éclat. Un éclat de paillasson tient sur le bord.

## Arc dramatique

- Monde : jardin, table, menthe, paillasson, puis porte de l'école.
- Désir : finir le soleil pour Nina, maintenant.
- Objet : dessin, galet, goutte, arrosoir, puis dessin mouillé.
- Indice unique : éclat de paillasson, vu dès l'ouverture, payé sur le bord. Pas éclat de galet / arrosoir.
- Urgence douce : elle souffle trop vite sur le jaune.
- Imprévu 1 : goutte, jaune qui s'étale, sourire parti, larmes.
- Cue : papa à la même hauteur. Un merci vécu, après le câlin.
- Imprévu 2 (plus rusé) : Nina part plus tôt, le dessin n'a pas séché, il glisse.
- Résolution : elle refuse de foncer, observe, écoute la porte, retrouve l'éclat, demande un câlin.
- Retour : tache d'eau, dessin contre Sarah, éclat sur le bord. Dénouement qui a failli : Nina part, le jaune n'a pas séché.

## Vécu

Sarah veut finir **maintenant**. Impatience, puis goutte, sourire parti. Elle dit je suis triste, pleure, demande un câlin. Maman ouvre les bras. Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : rester sans se presser, tenir le papier mouillé, ne pas courir après Nina. Merci vécu. Fin : l'éclat du début tient sur le bord.

## Vu et corrigé

- Titre : Sarah et le dessin mouillé (noyau dump). Relance : Que peut-elle faire ? expected triste.
- Lieu du dump-meta (jardin, puis porte de l'école). Maman et papa. Sarah = héros enfant-f. Nina = copine. Dump dessin / goutte / arrosoir / galet.
- Ouverture inventée (Sarah connaît la table, coin qui brille autrement), pas un gabarit v2, pas « Chloé est dans le jardin », pas « L'histoire est finie ».
- Indice unique : éclat de paillasson ×4. BAN éclat de galet / arrosoir / vitre / crayon / gomme / sac / cartable. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme/toute calme et `aujourd'hui` retirés. Strip dump « encore humide », « tout doucement », « le câlin est chaud, encore ».
- Leçon non dite : on la voit quand les yeux sont chauds, quand Sarah dit je suis triste, quand elle pleure, quand elle demande un câlin. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « j'ai dit : je suis ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Sarah est triste. Que peut-elle faire ? ». expected triste. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Chloé → Sarah. Hors Q : null.
- example4 063 / 095 / 027 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers Nina qui part.
- 804 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 804 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
