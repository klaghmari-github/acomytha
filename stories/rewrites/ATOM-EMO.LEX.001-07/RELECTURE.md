# ATOM-EMO.LEX.001-07 — Mila et la fraise tiède

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans
- **Leçon :** EMO.LEX.001 — nommer la joie + partager (vécue : fraise trop molle, jus aux doigts, sourire parti, papa accroupi, Mila s'arrête, tend, dit « je suis contente » ; 2e ruse : oiseau, jus, fraise molle dans le seau, elle refuse de foncer). JAMAIS dite en slogan. Pas « c'est de la joie ». Pas « j'ai dit : je suis ». Pas « tu as nommé ».
- **Personnages :** Mila, papa, maman. Mila = enfant-f (veut la fraise tiède maintenant). Dump Émeline → Mila. Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.
- **Lieu :** jardin, fraisiers, fin de journée, coin de la brouette. Dump : fraise, arrosoir, seau. Indice PAS fraise / arrosoir / seau / panier / treille / torchon.
- **Indice unique :** éclat de brouette (luit sur le fer → tremble à la fraise molle → luit quand l'oiseau se pose → tient sur le fer). BAN éclat de fraise / arrosoir / seau / panier / treille / moule / tuteur / saladier / gomme / berge / torchon / tabouret / tour.
- **Question moteur :** « Mila sourit. Que dit-elle ? » expected dump **content**. accepted dump `content | contente | je suis contente | joie | de la joie | partager`. retry dump Émeline → Mila : `Mila sent de la joie. Que dit-elle ?`. Hors Q : null. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Une goutte reste au bec de l'arrosoir. Seau mouillé. Sur le fer, un éclat de brouette luit. Mila veut la fraise tiède **maintenant**. Elle tire trop vite. Fraise trop molle. Jus. Sourire parti. Envie et peur. Papa s'accroupit. Elle s'arrête, tend, dit je suis contente. Merci vécu. Deuxième ruse : oiseau sur la brouette, jus dans le seau. Elle s'arrête, lit l'éclat. Un éclat de brouette tient sur le fer. La goutte tombe. Fin fragile.

## Arc dramatique

- Monde : jardin, fraisiers, fin de journée, arrosoir, seau, brouette, fer tiède.
- Désir : cueillir la fraise tiède, maintenant.
- Objet : fraise, arrosoir, seau. Coin nommé : le fer de la brouette.
- Indice unique : éclat de brouette, vu dès l'ouverture, payé sur le fer. Pas éclat de fraise / arrosoir / seau.
- Urgence douce : elle tire trop vite, trop fort.
- Imprévu 1 : fraise trop molle, jus aux doigts, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après qu'elle refuse de foncer vers le bout.
- Imprévu 2 (plus rusé) : oiseau sur la brouette, jus dans le seau, la fraise s'écrase.
- Résolution : elle refuse de foncer, observe, écoute le jardin, retrouve l'éclat, l'oiseau prend la goutte.
- Retour : trace de fraise sur le fer, goutte tombée, éclat qui tient. La fin a failli (jus, oiseau).

## Vécu

Mila veut prendre **maintenant**. Impatience, puis fraise molle, sourire parti. Elle s'arrête, tend, dit je suis contente. Papa se baisse, pose une question, ne récite pas le mot joie. Ils agissent : bouts tièdes, seau, oiseau, elle s'arrête. Merci vécu. Fin : l'éclat du début tient sur le fer.

## Vu et corrigé

- Titre : Mila et la fraise tiède (noyau dump). Relance : Que dit-elle ? expected content.
- Lieu du dump-meta (jardin, fraisiers, fin de journée). Maman et papa. Mila = héros enfant-f. Dump fraise / arrosoir / seau gardés comme objets, pas comme indice.
- Ouverture inventée (goutte au bec de l'arrosoir, fer tiède, éclat de brouette), pas un gabarit v2, pas « Émeline est dans le jardin ».
- Indice unique : éclat de brouette ×4. BAN éclat de fraise / arrosoir / seau / panier / treille / moule / tuteur / saladier / gomme / berge / torchon / tabouret / tour. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Q moteur sans tic.
- Leçon non dite : on la voit quand elle s'arrête, quand elle tend, quand elle dit je suis contente. Pas « c'est de la joie ». Pas « tu as nommé ». Une seule « je suis contente ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur conservée (Émeline → Mila). expected/accepted dump. retry Émeline → Mila. Hors Q : null. 5 chunks, kinds inchangés.
- example4 060 / 092 / 024 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers l'oiseau.
- 839 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 839 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
