# ATOM-EMO.LEX.001-03 — Nina et la cerise du matin

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans
- **Leçon :** EMO.LEX.001 — nommer la joie + partager (vécue : Nina veut la cerise **maintenant**, trop haute, sourire parti, papa accroupi ; une cerise plus bas, sourire ; « Je suis contente », elle tend, merci vécu ; 2e ruse : jus, branche trop haute, oiseau, elle refuse de foncer). JAMAIS dite dans le récit. Pas « c'est de la joie ». Pas « tu as nommé ». Pas « j'ai dit : je suis ».
- **Personnages :** Nina, papa, maman. Dump Emma/papa → D16 Nina = enfant-f (veut la cerise maintenant). Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.
- **Lieu :** jardin, cerisier, portail, cerise, noyau, tuteur, herbe, bois, soleil, panier. BAN treille / moule / fraise (LEX.001-01/02). Cerise/noyau/portail = dump.
- **Indice unique :** éclat de tuteur (luit à l'ouverture → tremble à la branche trop haute → luit au jus/oiseau → tient sur le bois). BAN éclat de cerise / noyau / portail / panier / grille / treille / moule / fraise / tour / comptoir / pot / rouleau / lit / étagère / torchon / tabouret.
- **Question moteur :** « Nina sourit. Que dit-elle ? » expected dump **content**. accepted dump `content | je suis contente | joie | de la joie | partager`. retry dump Emma → Nina. Non récitée dans les autres chunks. Hors Q : expected/accepted/retry restent **null**.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

L'air près du cerisier sent le sucre. Portail un peu ouvert. Sur le bois, un éclat de tuteur luit. Nina veut la cerise **maintenant**. Trop haute, doigts qui glissent. Sourire parti. Papa s'accroupit. Une cerise plus bas. Un sourire arrive. Je suis contente. Elle tend, merci vécu. Deuxième ruse : jus qui coule, branche trop haute, oiseau. Elle refuse de foncer. Noyau dans le panier. Un éclat de tuteur tient sur le bois.

## Arc dramatique

- Monde : jardin, cerisier, portail, tuteur, herbe froide, panier. ≠ treille / moule / fraise.
- Désir : cueillir la cerise du matin, maintenant.
- Objet : cerise, puis noyau, panier.
- Indice unique : éclat de tuteur, vu dès l'ouverture, payé sur le bois. Pas éclat de cerise / portail / panier.
- Urgence douce : elle saute trop vite vers la branche haute.
- Imprévu 1 : doigts qui glissent, cerise trop haute, sourire parti, poitrine trop vite.
- Cue : papa à la même hauteur. Un merci vécu, après le partage.
- Imprévu 2 (plus rusé) : jus qui coule, branche trop haute, oiseau.
- Résolution : elle refuse de foncer, observe, écoute le jardin, retrouve l'éclat, tend sans se presser.
- Retour : noyau dans le panier, portail un peu ouvert, éclat sur le bois.

## Vécu

Nina veut la cerise **maintenant**. Impatience, puis trop haute, sourire parti. Une cerise plus bas. Joues chaudes, ventre léger, sourire. Elle dit qu'elle est contente, tend un bout. Papa se baisse, pose une question, ne récite pas la règle. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Nina et la cerise du matin (noyau dump). Relance : Que dit-elle ? expected content.
- Lieu du dump-meta (jardin, cerisier). Maman et papa. Nina = héros enfant-f. Cerise / noyau / portail conservés.
- Ouverture inventée (air, sucre, portail ouvert), pas un gabarit v2, pas « Emma marche dans le jardin ».
- Indice unique : éclat de tuteur. BAN éclat de cerise / noyau / portail / panier / grille / treille / moule / fraise. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doucement », « c'est de la joie », « tu as nommé », « j'ai dit : je suis » du dump.
- Leçon non dite : on la voit quand le sourire arrive, quand Nina dit qu'elle est contente, quand elle tend. Pas « c'est de la joie ». Pas « tu as nommé ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Nina sourit. Que dit-elle ? ». expected content. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Emma → Nina.
- example4 056 / 088 / 020 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le jus et l'oiseau.
- 845 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 845 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
