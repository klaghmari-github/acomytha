# ATOM-EMO.LEX.003-06 — Le pique-nique de Nina

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans
- **Leçon :** EMO.LEX.003 — nommer la déception + autre idée (vécue : chaises mouillées, sourire parti, poitrine qui se bouscule, papa accroupi, Nina dit « je suis déçue », propose le salon ; 2e ruse : plus de fraises, le bol glisse, elle refuse de foncer, propose une poire). JAMAIS dite en slogan. Pas « j'ai dit : je suis ». Pas « tu as nommé ». Pas « un souhait peut attendre ». Pas « on peut chercher une autre idée ». Pas « ce n'est pas honteux ».
- **Personnages :** Nina, papa, maman. Dump Fanny → D16 Nina = enfant-f (veut le pique-nique dehors maintenant). Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.
- **Lieu :** maison, jour de pluie, salon. Coin nommé : le coin du napperon, au salon. Dump : pluie, pique-nique, fraises, poire (objets, pas indice). Indice PAS nappe / tapis / canapé / vitre / poire / fraise.
- **Indice unique :** éclat de napperon (luit sur le tissu → tremble aux chaises mouillées → luit au climax des fraises → tient sur le tissu). BAN éclat de nappe / tapis / canapé / store / cagette / kiosque / pelle / ficelle / poire / vitre.
- **Question moteur :** « La pluie arrive. Que dit Nina ? » expected dump **déçue**. accepted dump `déçue | je suis déçue | autre idée | une poire | une autre idée`. retry dump Fanny → Nina : `Nina cherche une autre idée. Que dit-elle d'abord ?`. Hors Q : null. Non récitée ailleurs.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

L'anse du panier pince le pouce de Nina. Pain, napperon, chaises mouillées. Sur le tissu, un éclat de napperon luit. Nina veut le pique-nique dehors **maintenant**. La pluie court sous la porte. Sourire parti. Envie et inquiétude. Papa s'accroupit. Je suis déçue. Merci vécu. Pique-nique au salon, croûte, tasses. Deuxième ruse : plus de fraises, le bol glisse. Elle s'arrête, lit l'éclat, propose une poire. La poire a failli glisser. Un éclat de napperon tient sur le tissu.

## Arc dramatique

- Monde : maison, jour de pluie, panier, napperon, chaises du jardin, fenêtre, salon.
- Désir : un pique-nique dehors, maintenant.
- Objet : panier, napperon, pain, fraises manquantes, poire à la trace.
- Indice unique : éclat de napperon, vu dès l'ouverture, payé sur le tissu. Pas éclat de nappe / tapis / canapé / store / vitre / poire / fraise.
- Urgence douce : elle avance trop vite vers la porte.
- Imprévu 1 : pluie, chaises trop mouillées, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après qu'elle refuse de foncer et propose le salon.
- Imprévu 2 (plus rusé) : plus de fraises, le bol glisse, la poire a failli glisser.
- Résolution : elle refuse de foncer, observe, écoute le salon, retrouve l'éclat, propose une poire.
- Retour : poire à la trace, napperon au milieu du salon, éclat sur le tissu. La fin a failli (bol qui glisse, poire qui part).

## Vécu

Nina veut le pique-nique **maintenant**. Impatience, puis pluie, sourire parti. Elle dit je suis déçue. Papa se baisse, pose une question, ne récite pas la leçon. Ils agissent : napperon au salon, puis bol vide, elle s'arrête. Merci vécu. Fin : l'éclat du début tient sur le tissu.

## Vu et corrigé

- Titre : Le pique-nique de Nina (noyau dump). Relance : Que dit Nina ? expected déçue.
- Lieu du dump-meta (maison, jour de pluie). Maman et papa. Nina = héros enfant-f. Dump pluie / pique-nique / fraises / poire gardés comme objets, pas comme indice.
- Ouverture inventée (anse du panier qui pince), pas un gabarit v2, pas gouttière/buée du dump, pas « Fanny joue au salon ».
- Indice unique : éclat de napperon ×4. BAN éclat de nappe / tapis / canapé / store / cagette / kiosque / pelle / ficelle / poire / vitre. Pas tache/flèche/marque/symbole. Pas nappe (napperon à la place).
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « j'ai dit : je suis ». Strip « on peut chercher une autre idée ». Strip « ce n'est pas honteux ».
- Leçon non dite : on la voit quand les chaises sont mouillées, quand elle dit je suis déçue, quand elle propose le salon, quand elle propose une poire. Pas « tu as nommé ». Une seule « je suis déçue ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « La pluie arrive. Que dit Nina ? ». expected/accepted dump. retry Fanny → Nina. Hors Q : null. 5 chunks, kinds inchangés.
- example4 073 / 005 / 037 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le bol qui glisse.
- 791 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 791 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
