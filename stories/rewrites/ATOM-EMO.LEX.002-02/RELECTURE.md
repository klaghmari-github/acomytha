# ATOM-EMO.LEX.002-02 — Nino et le bateau de papier

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans
- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un câlin (vécue : Nino dit « je suis triste », pleure, demande un câlin ; bateau emporté, papier déchiré, poitrine trop vite, sourire parti, papa accroupi ; 2e ruse : papier qui se déchire plus loin, bateau qui part, il refuse de foncer). JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». Pas « tu as nommé ». Pas « j'ai dit : je suis ».
- **Personnages :** Nino, papa, maman. Nino = enfant-m. Pas de copain. Troupe D16. Pas de maîtresse.
- **Lieu :** parc, après la pluie, flaque, bateau, papier, capuche, allée, herbe, manteau, poche, tissu. BAN banc / grille / tapis (indice et mot). Bateau / flaque / papier = dump.
- **Indice unique :** éclat de capuche (luit à l'ouverture → tremble à la déchirure → luit quand le bateau part → tient sur le tissu). BAN éclat de flaque / bateau / papier / grille / banc / tapis.
- **Question moteur :** « Nino a les yeux chauds. Que dit-il ? » expected dump **triste**. accepted dump `triste | je suis triste | câlin | un câlin | pleurer`. retry dump gardé. Non récitée dans les autres chunks. Hors Q : expected / accepted / retry = null.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Une goutte tape la capuche. Un détail paraît : sur le tissu, un éclat de capuche luit. Bateau de papier, flaque ronde. Il veut le bateau **maintenant**. L'eau l'emporte. Le papier se déchire. Poitrine trop vite. Sourire parti. Yeux chauds. « je suis triste ». Il pleure. Papa s'accroupit. Merci vécu, après le câlin. Deuxième ruse : papier qui se déchire plus loin, bateau qui part. Il s'arrête, lit l'éclat, demande un câlin. Un éclat de capuche tient sur le tissu.

## Arc dramatique

- Monde : parc après la pluie, goutte sur la capuche, allée, herbe lourde.
- Désir : faire partir le bateau de papier, maintenant.
- Objet : bateau, papier, flaque (objets dump, pas l'indice).
- Indice unique : éclat de capuche, vu dès l'ouverture, payé sur le tissu. Pas éclat de flaque / bateau / papier.
- Urgence douce : il pose le bateau trop vite.
- Imprévu 1 : l'eau emporte, le papier se déchire, poitrine trop vite, sourire parti, yeux chauds.
- Cue : papa à la même hauteur. Un merci vécu, après le câlin.
- Imprévu 2 (plus rusé) : le papier se déchire plus loin, le bateau part vers le milieu.
- Résolution : il refuse de foncer, observe, écoute le parc, retrouve l'éclat, demande un câlin.
- Retour : bateau un peu déchiré, goutte sur la capuche, éclat sur le tissu.

## Vécu

Nino veut le bateau **maintenant**. Il dit « je suis triste » (acte, une fois). Il pleure. Impatience, puis bateau parti, sourire parti. Il s'arrête, observe. Papa se baisse, pose une question, ne récite pas la règle. Papier qui se déchire plus loin, bateau qui part. Il refuse de foncer. Il demande un câlin. Merci vécu. Fin : l'éclat du début tient sur le tissu.

## Vu et corrigé

- Titre : Nino et le bateau de papier (noyau dump). Relance : Que dit-il ? expected triste.
- Lieu du dump-meta (parc, après la pluie). Maman et papa. Nino = héros enfant-m.
- Ouverture inventée (goutte sur la capuche), pas un gabarit v2, pas « Après la pluie, le parc sent », pas « Nino est au parc ».
- Indice unique : éclat de capuche. BAN éclat de flaque / bateau / papier / grille / banc / tapis. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doucement » du dump. BAN banc / grille / tapis.
- Leçon non dite : on la voit quand il dit « je suis triste », quand il pleure, quand il demande un câlin. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». Pas « tu as nommé ». Pas « j'ai dit : je suis ». Pas « L'histoire est finie ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Nino a les yeux chauds. Que dit-il ? ». expected triste. 5 chunks, kinds inchangés. expected/accepted/retry dump conservés. Hors Q : null.
- example4 062 / 094 / 026 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2 / raw.js.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le bateau qui part.
- 801 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 801 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
