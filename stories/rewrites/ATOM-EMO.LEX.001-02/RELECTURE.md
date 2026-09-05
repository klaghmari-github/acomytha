# ATOM-EMO.LEX.001-02 — Raphaël et le gâteau à la vanille

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans
- **Leçon :** EMO.LEX.001 — nommer la joie + partager (vécue : Raphaël dit « je suis content », tend la fraise ; moule penche, poitrine trop vite, sourire parti, papa accroupi ; 2e ruse : gâteau trop chaud, fraise qui glisse, il refuse de foncer). JAMAIS dite dans le récit. Pas « c'est de la joie ». Pas « tu as nommé ». Pas « j'ai dit : je suis ».
- **Personnages :** Raphaël, papa, maman. Dump Ava → D16 Raphaël = enfant-m. Pas de copain. Troupe D16. Pas de maîtresse.
- **Lieu :** cuisine, après-midi de pluie, moule, gâteau, vanille, fraise, vitre, table, four, métal. BAN tasse / nappe / farine / casserole / assiette / tour / comptoir / pot / rouleau / lit / étagère / torchon / tabouret / treille (indice). ≠ dump vanille qui monte l'escalier.
- **Indice unique :** éclat de moule (luit à l'ouverture → tremble à la pente → luit quand la fraise glisse → tient sur le métal). BAN éclat de fraise / vanille / tasse / nappe / farine / casserole / assiette / tour / comptoir.
- **Question moteur :** « Raphaël sourit. Que dit-il ? » expected dump **content**. accepted dump `content | contente | je suis contente | joie | de la joie`. retry dump Ava → Raphaël, dit-il. Non récitée dans les autres chunks. Hors Q : expected / accepted / retry = null.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

La pluie tapote la vitre. Raphaël connaît la cuisine. Un détail paraît nouveau : sur le métal, un éclat de moule luit. Vanille, gâteau, fraises. Il veut le gâteau **maintenant**. Joues chaudes, sourire, « je suis content ». Il tire le moule trop vite. Le moule penche. Poitrine trop vite. Sourire parti. Papa s'accroupit. Merci vécu, après la fraise tendue. Deuxième ruse : gâteau trop chaud, fraise qui glisse. Il s'arrête, lit l'éclat. Un éclat de moule tient sur le métal.

## Arc dramatique

- Monde : cuisine, après-midi de pluie, vitre, four, moule, table collante.
- Désir : prendre le gâteau à la vanille, maintenant.
- Objet : moule, gâteau, fraises (objets dump, pas l'indice).
- Indice unique : éclat de moule, vu dès l'ouverture, payé sur le métal. Pas éclat de fraise / vanille / tasse.
- Urgence douce : il tire le moule trop vite.
- Imprévu 1 : moule penche, gâteau coincé, poitrine trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après la fraise tendue.
- Imprévu 2 (plus rusé) : gâteau trop chaud, fraise qui glisse.
- Résolution : il refuse de foncer, observe, écoute la cuisine, retrouve l'éclat, tend la fraise.
- Retour : partage fragile, moule près de la table, éclat sur le métal.

## Vécu

Raphaël veut le gâteau **maintenant**. Il dit « je suis content » (acte, une fois). Impatience, puis moule penché, sourire parti. Il s'arrête, observe. Papa se baisse, pose une question, ne récite pas la règle. Gâteau trop chaud, fraise qui glisse. Il refuse de foncer. Il tend la fraise. Merci vécu. Fin : l'éclat du début tient sur le métal.

## Vu et corrigé

- Titre : Raphaël et le gâteau à la vanille (noyau dump). Relance : Que dit-il ? expected content.
- Lieu du dump-meta (cuisine, après-midi de pluie). Maman et papa. Raphaël = héros enfant-m. Dump Ava retiré.
- Ouverture inventée (vitre, cuisine connue, détail nouveau), pas un gabarit v2, pas « La vanille monte l'escalier ».
- Indice unique : éclat de moule. BAN éclat de fraise / vanille / tasse / nappe / farine / casserole / assiette / tour / comptoir. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doucement » du dump.
- Leçon non dite : on la voit quand il dit « je suis content », quand il tend la fraise. Pas « c'est de la joie ». Pas « tu as nommé ». Pas « j'ai dit : je suis ». Pas « L'histoire est finie ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Raphaël sourit. Que dit-il ? ». expected content. 5 chunks, kinds inchangés. expected/accepted dump conservés (féminin moteur gardé). retry Ava → Raphaël, dit-il. Hors Q : null.
- example4 055 / 087 / 019 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2 / raw.js.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers la fraise qui glisse.
- 764 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 764 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
