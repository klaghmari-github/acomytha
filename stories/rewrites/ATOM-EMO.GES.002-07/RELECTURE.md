# ATOM-EMO.GES.002-07 — Le cube rouge d'Amir

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** EMO.GES.002 — souffler, faire une pause (vécue : cubes tombent, poitrine trop vite, sourire parti, papa accroupi, Amir souffle, s'assoit, pause ; 2e ruse : la tour semble tenir, un pied accroche le torchon, un cube glisse, il refuse de foncer). JAMAIS dite dans le récit. Pas « on peut souffler ». Pas « tu peux souffler ». Pas « il faut souffler ». Pas « c'est bien de faire une pause ».
- **Personnages :** Amir, papa, maman. Dump Amir/papa/maman. Amir = enfant-m (veut la tour maintenant). Pas de copain (dump sans camarade). Troupe D16. Pas de Géraldine. Pas de maîtresse.
- **Lieu :** chambre, plancher, torchon, boîte, cubes, bois, rayon, pli, porte. BAN tapis / rideau / coussin / canapé / farine. ≠ 002-01 salon / carton. ≠ 002-05 lit / coton. ≠ 002-06 étagère / cire.
- **Indice unique :** éclat de torchon (luit à l'ouverture → tremble à la chute → luit quand la tour semble tenir → tient sur le pli). BAN éclat de cube / tapis / tour / lit / comptoir / étagère.
- **Question moteur :** « La tour tombe. Que fait Amir ? » expected dump **souffler**. accepted dump `souffler | elle souffle | pause | une pause | s'asseoir` → `il souffle` (Amir). retry dump « Elle souffle. Elle s'assoit. Que fait-elle ? » → « Il souffle. Il s'assoit. Que fait-il ? ». Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Une bande rouge barre le torchon plié. Cube rouge. Sur le pli, un éclat de torchon luit. Boîte, plancher tiède, chambre claire. Amir veut la tour **maintenant**. Les cubes tombent. Poitrine trop vite. Sourire parti. Papa s'accroupit. Il souffle, pause. Merci vécu. Deuxième ruse : la tour semble tenir, un pied accroche, un cube glisse. Il s'arrête, lit l'éclat. Un éclat de torchon tient sur le pli.

## Arc dramatique

- Monde : chambre, torchon, plancher, boîte, cubes, bois.
- Désir : empiler la tour, maintenant.
- Objet : cubes rouges, puis tour qui tombe.
- Indice unique : éclat de torchon, vu dès l'ouverture, payé sur le pli. Pas éclat de cube / tapis / tour.
- Urgence douce : il pose trop vite, trop haut.
- Imprévu 1 : cubes tombent, poitrine trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après la pause.
- Imprévu 2 (plus rusé) : la tour semble tenir, un pied accroche le torchon, un cube glisse au bas.
- Résolution : il refuse de foncer, observe, écoute la chambre, retrouve l'éclat, souffle, attend.
- Retour : poumf, tour près de la boîte, éclat sur le pli.

## Vécu

Amir veut la tour **maintenant**. Impatience, puis cubes par terre, sourire parti. Il souffle, s'assoit, les mains sur les genoux. Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : un cube sans se presser, tour de deux. Merci vécu. Fin : l'éclat du début tient sur le pli.

## Vu et corrigé

- Titre : Le cube rouge d'Amir (noyau dump). Relance : Que fait Amir ? expected souffler.
- Lieu du dump-meta (chambre). Maman et papa. Amir = héros enfant-m. BAN tapis / coussin dans le récit.
- Ouverture inventée (bande rouge sur le torchon), pas un gabarit v2, pas « Le soleil chauffe le plancher » du source, pas « Amir joue dans la chambre ».
- Indice unique : éclat de torchon. BAN éclat de cube / tapis / tour / lit / comptoir. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doux » du dump.
- Leçon non dite : on la voit quand les cubes tombent, quand la poitrine va trop vite, quand Amir souffle, quand il s'assoit. Pas « on peut souffler ». Pas « tu as fait une pause ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « La tour tombe. Que fait Amir ? ». expected souffler. 5 chunks, kinds inchangés. expected dump conservé. accepted/retry elle → il (Amir).
- example4 052 / 084 / 016 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers la tour qui semble tenir.
- 827 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 827 mots
- `text` = `script` collé
- Q dump : La tour tombe. Que fait Amir ?
- Indice ×4 : éclat de torchon (luit / tremble / luit / tient)
- TTS 5/5

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
